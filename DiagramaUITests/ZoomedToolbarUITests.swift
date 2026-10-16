import XCTest

/// Taps the drawing toolbar in a zoomed-in view, the way a learner does. The zoomed picture
/// is bigger than its box, and once caught the taps meant for these buttons.
final class ZoomedToolbarUITests: XCTestCase {
    private var app: XCUIApplication!

    override func setUp() {
        continueAfterFailure = false
        app = XCUIApplication()
        // The fish lesson's "Eye and mouth" step zooms in on the predator's eye.
        app.launchArguments = ["-openLesson", "g3-school-of-fish", "-step", "2"]
        app.launch()
    }

    private func scribble() {
        let canvas = app.descendants(matching: .any)["Drawing area"].firstMatch
        XCTAssertTrue(canvas.waitForExistence(timeout: 10))
        let start = canvas.coordinate(withNormalizedOffset: CGVector(dx: 0.3, dy: 0.3))
        let end = canvas.coordinate(withNormalizedOffset: CGVector(dx: 0.7, dy: 0.6))
        start.press(forDuration: 0.05, thenDragTo: end)
    }

    func testEraserSwitchesOnWhenZoomed() {
        scribble()
        let eraser = app.buttons["Eraser"]
        XCTAssertTrue(eraser.waitForExistence(timeout: 5))
        eraser.tap()
        XCTAssertTrue(app.buttons["Eraser on"].waitForExistence(timeout: 2), "The eraser didn't switch on")

        // Rubbing out hands the pen back automatically.
        scribble()
        XCTAssertTrue(app.buttons["Eraser"].waitForExistence(timeout: 2), "The pen didn't come back after erasing")
    }

    func testUndoAndMoreMenuRespondWhenZoomed() {
        scribble()
        let undo = app.buttons["Undo"]
        XCTAssertTrue(undo.waitForExistence(timeout: 5))
        XCTAssertTrue(undo.isEnabled)
        undo.tap()

        app.buttons["More"].tap()
        XCTAssertTrue(app.buttons["Restart step"].waitForExistence(timeout: 2), "The ⋯ menu didn't open")
    }
}
