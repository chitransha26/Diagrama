import Foundation
import PostHog
import SwiftUI

/// Product analytics (PostHog). Learners can be children, so this sends only what's needed
/// to improve lessons: no person profiles, no autocapture of taps or screens, no session
/// replay, and never anything the learner types. Off when no token is configured
/// (Config/Secrets.xcconfig) and during automated test runs.
enum Analytics {
    nonisolated(unsafe) private static var enabled = false

    static func setup() {
        guard !isAutomatedRun,
              let token = Bundle.main.object(forInfoDictionaryKey: "PostHogProjectToken") as? String,
              token.hasPrefix("phc_"),
              let host = Bundle.main.object(forInfoDictionaryKey: "PostHogHost") as? String,
              host.hasPrefix("https://") else { return }
        let config = PostHogConfig(apiKey: token, host: host)
        config.personProfiles = .identifiedOnly   // we never identify anyone
        config.captureApplicationLifecycleEvents = true
        config.captureScreenViews = false          // screens are named by hand below
        config.captureElementInteractions = false
        config.sessionReplay = false
        // POSTHOG_DEBUG=1 in the launch environment logs what's sent, for checking setup.
        config.debug = ProcessInfo.processInfo.environment["POSTHOG_DEBUG"] != nil
        PostHogSDK.shared.setup(config)
        enabled = true
    }

    /// Unit and UI tests, and the debug launch arguments used to check lessons on a
    /// simulator, shouldn't count as real use.
    private static var isAutomatedRun: Bool {
        let info = ProcessInfo.processInfo
        return info.environment["XCTestConfigurationFilePath"] != nil
            || info.arguments.contains { ["-openLesson", "-autodraw", "-step"].contains($0) }
    }

    static func screen(_ name: String, _ properties: [String: Any] = [:]) {
        guard enabled else { return }
        PostHogSDK.shared.screen(name, properties: properties)
    }

    static func track(_ event: String, _ properties: [String: Any] = [:]) {
        guard enabled else { return }
        PostHogSDK.shared.capture(event, properties: properties)
    }

    // MARK: Lesson context, attached to every event while a lesson is open

    static func lessonProperties(_ lesson: Lesson) -> [String: Any] {
        ["lesson_id": lesson.id, "lesson_title": lesson.title, "grade": lesson.grade,
         "grade_band": lesson.band.rawValue, "subject": lesson.subject.rawValue, "standard": lesson.standard]
    }

    static func enterLesson(_ lesson: Lesson) {
        guard enabled else { return }
        PostHogSDK.shared.register(lessonProperties(lesson))
    }

    static func enterStep(_ index: Int, of lesson: Lesson) {
        guard enabled, lesson.steps.indices.contains(index) else { return }
        let step = lesson.steps[index]
        PostHogSDK.shared.register(["step_index": index, "step_type": step.kind.analyticsName, "step_title": step.title])
    }

    static func leaveLesson() {
        guard enabled else { return }
        for key in ["lesson_id", "lesson_title", "grade", "grade_band", "subject", "standard",
                    "step_index", "step_type", "step_title"] {
            PostHogSDK.shared.unregister(key)
        }
    }
}

extension StepKind {
    /// A stable name for the kind of step, for analytics.
    var analyticsName: String {
        switch self {
        case .trace(_, let part): part == .details ? "trace_details" : "trace"
        case .color: "color"
        case .label: "label"
        case .choice: "choice"
        case .order: "order"
        case .identify: "identify"
        case .drawLewis: "draw_lewis"
        case .recall: "draw_from_memory"
        case .copy: "copy"
        }
    }
}

extension View {
    /// Records a screen view each time this screen appears.
    func analyticsScreen(_ name: String, _ properties: [String: Any] = [:]) -> some View {
        onAppear { Analytics.screen(name, properties) }
    }
}
