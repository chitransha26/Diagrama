import SwiftUI

@main
struct DiagramaApp: App {
    @State private var store = ProgressStore()

    var body: some Scene {
        WindowGroup {
            TabView {
                LearnView()
                    .tabItem { Label("Learn", systemImage: "pencil.and.scribble") }
                GalleryView()
                    .tabItem { Label("Gallery", systemImage: "square.grid.2x2") }
            }
            .environment(store)
            .tint(Theme.indigo)
        }
    }
}
