import Foundation

enum LabelGrader {
    static func normalize(_ s: String) -> String {
        s.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
    }

    /// Accepts the expected term or any listed synonym (PRD §03: "cell membrane" = "plasma membrane").
    static func isCorrect(_ answer: String, for target: LabelTarget) -> Bool {
        let a = normalize(answer)
        return ([target.answer] + target.synonyms).contains { normalize($0) == a }
    }

    /// Names the error and why it matters, rather than just marking it wrong (PRD §05).
    static func explanation(for answer: String, target: LabelTarget, step: LabelStep) -> String {
        let a = normalize(answer)
        if let specific = target.mistakes.first(where: { normalize($0.key) == a })?.value { return specific }
        if let common = step.commonMistakes.first(where: { normalize($0.key) == a })?.value { return common }
        return "This isn't the \(answer.lowercased()). Look at where the marker sits and what it touches."
    }
}
