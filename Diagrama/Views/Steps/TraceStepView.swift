import PencilKit
import SwiftUI

/// The tools row: the pen the app picked, plus eraser, undo and restart (as in ArtWorkout).
struct DrawingToolbar: View {
    let pen: Pen
    @Binding var erasing: Bool
    var canUndo: Bool
    var enabled = true
    let onUndo: () -> Void
    let onRestart: () -> Void

    var body: some View {
        HStack(spacing: 10) {
            Label(pen.name, systemImage: pen.symbol)
                .font(.subheadline.weight(.semibold))
                .padding(.horizontal, 12)
                .padding(.vertical, 7)
                .background(Capsule().fill(erasing ? Color(.tertiarySystemFill) : Theme.indigo.opacity(0.14)))
                .foregroundStyle(erasing ? .secondary : Theme.indigo)
                .accessibilityLabel("\(pen.name), picked for this step")
                .onTapGesture { erasing = false }

            Spacer()

            Button {
                erasing.toggle()
            } label: {
                Image(systemName: erasing ? "eraser.fill" : "eraser")
                    .frame(width: 36, height: 30)
            }
            .buttonStyle(.bordered)
            .tint(erasing ? Theme.indigo : .secondary)
            .accessibilityLabel(erasing ? "Eraser on" : "Eraser")

            Button(action: onUndo) {
                Image(systemName: "arrow.uturn.backward").frame(width: 36, height: 30)
            }
            .buttonStyle(.bordered)
            .tint(.secondary)
            .disabled(!canUndo)
            .accessibilityLabel("Undo")

            Menu {
                Button("Restart step", systemImage: "arrow.counterclockwise", action: onRestart)
            } label: {
                Image(systemName: "ellipsis").frame(width: 36, height: 30)
            }
            .buttonStyle(.bordered)
            .tint(.secondary)
            .accessibilityLabel("More")
        }
        .disabled(!enabled)
    }
}

/// Fills as the guide is traced: green for ink on the guide, red for ink off it (ArtWorkout).
struct TraceProgressBar: View {
    let result: TraceResult?

    var body: some View {
        let r = result ?? .empty
        let good = r.coverage * r.precision
        let bad = min(1 - good, r.coverage * (1 - r.precision))
        GeometryReader { geo in
            ZStack(alignment: .leading) {
                Capsule().fill(Color(.tertiarySystemFill))
                HStack(spacing: 0) {
                    Rectangle().fill(Theme.lime).frame(width: geo.size.width * good)
                    Rectangle().fill(Theme.coral).frame(width: geo.size.width * bad)
                }
                .clipShape(Capsule())
            }
        }
        .frame(height: 12)
        .animation(.easeOut(duration: 0.25), value: r)
        .accessibilityElement()
        .accessibilityLabel("Traced \(Int(r.coverage * 100)) percent, \(Int((1 - r.precision) * 100)) percent of your line off the guide")
    }
}

/// Guided tracing on its own layer: demo stroke, dashed guide, live progress, and a
/// restart prompt when more of the line is off the guide than on it.
struct TraceStepView: View {
    @Bindable var session: LessonSession
    let structureID: String
    let part: TracePart

    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var drawing = PKDrawing()
    @State private var result: TraceResult?
    @State private var passed = false
    @State private var demo: CGFloat = 0
    @State private var lastWasPencil = false
    @State private var erasing = false
    @State private var corrected = false
    @State private var fullSide: CGFloat = 0
    /// Which zoomed piece is being drawn, and the first stroke that belongs to it.
    @State private var segment = 0
    @State private var segmentStart = 0
    @State private var segmentScores: [Double] = []
    @State private var advancing = false

    private var structure: Structure { session.lesson.structure(structureID) }
    private var segments: [(guides: [Polyline], focus: CGRect?)] { structure.segments(part) }
    private var guides: [Polyline] { segments[segment].guides }
    /// Every piece shares the first piece's zoom, so the canvas's coordinates never change.
    private var viewport: Viewport {
        let first = Viewport(focus: segments[0].focus)
        guard let f = segments[segment].focus, first.zoom > 1 else { return first }
        return Viewport(center: CGPoint(x: f.midX, y: f.midY), zoom: first.zoom)
    }
    private var needsRestart: Bool {
        guard let r = result, !passed else { return false }
        return r.precision < StrokeScorer.restartBelow && r.coverage > 0.2
    }

    var body: some View {
        VStack(spacing: 10) {
            DrawingToolbar(
                pen: structure.pen, erasing: $erasing, canUndo: drawing.strokes.count > segmentStart, enabled: !passed,
                onUndo: undo, onRestart: restart
            )
            HStack(spacing: 10) {
                TraceProgressBar(result: result)
                if segments.count > 1 {
                    Text("\(min(segment + 1, segments.count)) of \(segments.count)")
                        .font(.caption.weight(.semibold)).monospacedDigit()
                        .foregroundStyle(.secondary)
                }
            }

            SquareStage { side in
                ZoomedStage(viewport: viewport, side: side) { full in
                    ZStack {
                        DiagramView(
                            lesson: session.lesson, revealed: session.revealed, filled: session.filled,
                            templateOpacity: session.layers.isEmpty ? 0.8 : 0.25,
                            guides: passed ? [] : guides,
                            offGuide: result?.offGuidePoints ?? [],
                            untraced: passed ? [] : result?.untraced ?? []
                        )
                        InkLayers(session: session, viewport: viewport)
                        if !passed, let first = guides.first {
                            GuideDemo(guide: first, progress: demo)
                        }
                        InkCanvas(
                            drawing: $drawing,
                            tool: erasing ? Eraser.tool : structure.pen.tool,
                            isEnabled: !passed,
                        onLift: { if erasing { DispatchQueue.main.async { erasing = false } } }
                        ) { added, isPencil in
                            if erasing { corrected = true } else if added { lastWasPencil = isPencil }
                            evaluate()
                        }
                        if !passed {
                            PartNameTag(
                                name: session.step.title,
                                target: guides.map(\.bounds).reduce(CGRect.null) { $0.union($1) },
                                viewport: viewport
                            )
                            .transition(.opacity)
                        }
                    }
                    .onAppear { fullSide = full }
                    .onChange(of: full) { _, new in fullSide = new }
                }
            }

            feedback

            ContinueButton(enabled: passed) {
                session.addLayer(drawing, canvasSide: fullSide)
                session.recordTrace(TraceRecord(
                    match: segmentScores.isEmpty ? 0 : segmentScores.reduce(0, +) / Double(segmentScores.count),
                    smoothness: StrokeScorer.smoothness(strokes: drawing.strokes.flatMap(\.visibleScreenSegments)),
                    firstTry: !corrected
                ))
                session.advance()
            }
        }
        .onAppear { playDemo(after: 0.4) }
        #if DEBUG
        .task(id: segment) { await autodrawForTesting() }
        #endif
    }

    #if DEBUG
    /// With the `-autodraw` launch argument, traces each guide perfectly, so later steps can
    /// be checked quickly in the simulator. Debug builds only.
    private func autodrawForTesting() async {
        guard ProcessInfo.processInfo.arguments.contains("-autodraw") else { return }
        try? await Task.sleep(for: .seconds(0.6))
        guard fullSide > 0, !passed else { return }
        let scale = fullSide / DiagramSpace.size
        for g in guides {
            let pts = g.closed ? g.points + [g.points[0]] : g.points
            let tool = structure.pen.tool
            let stroke = PKStroke(ink: PKInk(tool.inkType, color: tool.color), path: PKStrokePath(
                controlPoints: pts.enumerated().map { i, p in
                    PKStrokePoint(location: CGPoint(x: p.x * scale, y: p.y * scale), timeOffset: Double(i) * 0.01,
                                  size: CGSize(width: tool.width, height: tool.width), opacity: 1, force: 1, azimuth: 0, altitude: .pi / 2)
                },
                creationDate: .now))
            drawing.strokes.append(stroke)
        }
        evaluate()
    }
    #endif

    @ViewBuilder private var feedback: some View {
        ScrollView {
        VStack(alignment: .leading, spacing: 8) {
            if passed, let note = session.step.note {
                NoteCard(title: session.step.title, note: note)
                    .transition(.scale(scale: 0.85, anchor: .bottom).combined(with: .opacity))
            } else if needsRestart {
                FeedbackRow(kind: .wrong, text: "More of your line is off the guide than on it. Restart this step and follow the dashed line.")
                Button("Restart step", systemImage: "arrow.counterclockwise", action: restart)
                    .buttonStyle(.bordered)
            } else if let r = result {
                FeedbackRow(kind: passed ? .correct : .info, text: message(for: r))
            } else {
                FeedbackRow(kind: .info, text: session.step.instruction)
            }
        }
        }
        .scrollBounceBehavior(.basedOnSize)
        // Fixed height so the canvas never shifts or resizes under the learner's hand.
        .frame(height: 156, alignment: .top)
    }

    private func evaluate() {
        guard fullSide > 0 else { return }
        let scale = fullSide / DiagramSpace.size
        let pts = drawing.strokes.dropFirst(segmentStart).flatMap { $0.diagramSegments(scale: scale) }
        guard !pts.isEmpty else { result = nil; return }
        let r = StrokeScorer.score(
            strokes: pts, guides: guides,
            tolerance: StrokeScorer.tolerance(isPencil: lastWasPencil, scale: scale)
        )
        result = r
        guard !advancing, StrokeScorer.isComplete(r) else { return }
        segmentScores.append(r.score)
        if segment + 1 < segments.count {
            advancing = true
            // Move the zoom on to the next piece, as ArtWorkout does between parts.
            Task { @MainActor in
                try? await Task.sleep(for: .seconds(0.5))
                withAnimation(.easeInOut(duration: 0.45)) {
                    segment += 1
                    segmentStart = drawing.strokes.count
                    result = nil
                }
                advancing = false
                playDemo(after: 0.5)
            }
        } else {
            withAnimation(.spring(response: 0.45, dampingFraction: 0.7)) {
                passed = true
                erasing = false
                session.revealed.insert(part.key(structureID))
            }
        }
    }

    private func undo() {
        guard drawing.strokes.count > segmentStart else { return }
        drawing.strokes.removeLast()
        corrected = true
        evaluate()
    }

    private func restart() {
        drawing = PKDrawing()
        segment = 0
        segmentStart = 0
        segmentScores = []
        result = nil
        corrected = true
        erasing = false
        playDemo(after: 0.2)
    }

    private func message(for r: TraceResult) -> String {
        let name = session.step.title
        if !passed, segments.count > 1, StrokeScorer.isComplete(r) {
            return "Good. On to the next one."
        }
        if passed {
            return r.precision >= 0.85
                ? "\(name) done. Very steady line!"
                : "\(name) done. The rings show where your line left the guide."
        }
        if r.precision < 0.75 {
            return "Keep going. Rings mark where your line left the guide; you can erase those parts."
        }
        let skipped = r.guideCoverage.filter { $0 < 0.5 }.count
        if skipped > 0, guides.count > 1 {
            return skipped == 1 ? "Keep going: one part hasn't been traced yet." : "Keep going: \(skipped) parts haven't been traced yet."
        }
        return r.coverage >= 0.85
            ? "Almost there. Trace over the blue marks to close the gaps."
            : "Keep going: follow the dashed line all the way."
    }

    private func playDemo(after delay: Double) {
        demo = 0
        guard !reduceMotion else { return }
        Task { @MainActor in
            try? await Task.sleep(for: .seconds(delay))
            withAnimation(.easeInOut(duration: 2.2)) { demo = 1 }
            try? await Task.sleep(for: .seconds(2.6))
            demo = 0
        }
    }
}

/// Drawing from memory with no guide, then compared with the reference (PRD §02, §05).
struct RecallStepView: View {
    @Bindable var session: LessonSession
    let structureIDs: [String]

    @State private var drawing = PKDrawing()
    @State private var lastWasPencil = false
    @State private var erasing = false
    @State private var side: CGFloat = 0
    @State private var result: TraceResult?
    @State private var passed = false
    @State private var peeked = false
    @State private var tries = 0

    private var guides: [Polyline] { structureIDs.flatMap { session.lesson.structure($0).outlines } }
    private var names: String {
        ListFormatter.localizedString(byJoining: structureIDs.map { session.lesson.structure($0).name })
    }

    var body: some View {
        VStack(spacing: 10) {
            DrawingToolbar(
                pen: .pen, erasing: $erasing, canUndo: !drawing.strokes.isEmpty, enabled: !passed,
                onUndo: { if !drawing.strokes.isEmpty { drawing.strokes.removeLast(); result = nil } },
                onRestart: { drawing = PKDrawing(); result = nil }
            )

            SquareStage { side in
                ZStack {
                    if peeked {
                        DiagramView(lesson: session.lesson, revealed: Set(structureIDs), filled: [])
                            .opacity(0.35)
                    } else {
                        Theme.paper
                    }
                    InkCanvas(
                        drawing: $drawing,
                        tool: erasing ? Eraser.tool : Pen.pen.tool,
                        isEnabled: !passed,
                        onLift: { if erasing { DispatchQueue.main.async { erasing = false } } }
                    ) { added, isPencil in
                        if added { lastWasPencil = isPencil }
                        result = nil
                    }
                }
                .onAppear { self.side = side }
                .onChange(of: side) { _, new in self.side = new }
            }

            VStack(alignment: .leading, spacing: 8) {
                if let r = result {
                    if passed {
                        FeedbackRow(kind: .correct, text: peeked
                                    ? "That matches. Next time, try it without peeking."
                                    : "Your \(names) match the real layout. Drawn from memory!")
                    } else {
                        FeedbackRow(kind: .wrong, text: "Not quite: only \(Int((r.coverage * 100).rounded()))% lines up with the \(names). Check the shapes and where they sit, then try again.")
                    }
                } else {
                    FeedbackRow(kind: .info, text: "Draw the \(names). Press Check when you're done.")
                }
            }
            .frame(height: 92, alignment: .top)

            HStack(spacing: 12) {
                if tries > 0 && !passed && !peeked {
                    Button {
                        peeked = true
                    } label: {
                        Label("Peek", systemImage: "eye")
                    }
                    .buttonStyle(.bordered)
                }
                Spacer()
                if passed || tries >= 3 {
                    ContinueButton {
                        session.recallPassed = passed && !peeked
                        session.advance()
                    }
                    .frame(maxWidth: 200)
                } else {
                    ContinueButton(title: "Check", enabled: !drawing.strokes.isEmpty) { check() }
                        .frame(maxWidth: 200)
                }
            }
        }
    }

    private func check() {
        guard side > 0 else { return }
        let scale = side / DiagramSpace.size
        let r = StrokeScorer.scoreRecall(
            strokes: drawing.strokes.flatMap { $0.diagramSegments(scale: scale) }, guides: guides,
            tolerance: StrokeScorer.tolerance(isPencil: lastWasPencil, scale: scale)
        )
        tries += 1
        result = r
        if StrokeScorer.recallPassed(r) {
            withAnimation { passed = true; erasing = false }
        }
    }
}
