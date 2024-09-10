#include <argparse/argparse.hpp>
#include <fmt/core.h>
#include <imgui.h>
#include <vector>

int main(int argc, char* argv[])
{
    argparse::ArgumentParser program("emusys", "0.0.1");

    try {
        program.parse_args(argc, argv);
    } catch (const std::runtime_error& err) {
        std::cerr << err.what() << std::endl;
        std::cerr << program;
        std::exit(1);
    }

    // This is from the imgui null example
    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImGuiIO& io = ImGui::GetIO();

    // Build atlas
    unsigned char* tex_pixels = NULL;
    int tex_w, tex_h;
    io.Fonts->GetTexDataAsRGBA32(&tex_pixels, &tex_w, &tex_h);

    for (int n = 0; n < 20; n++) {
        fmt::print("NewFrame() {}\n", n);
        io.DisplaySize = ImVec2(1920, 1080);
        io.DeltaTime = 1.0f / 60.0f;
        ImGui::NewFrame();

        static float f = 0.0f;
        ImGui::Text("Hello, world!");
        ImGui::SliderFloat("float", &f, 0.0f, 1.0f);
        ImGui::Text("Application average %.3f ms/frame (%.1f FPS)", 1000.0f / io.Framerate, io.Framerate);
        ImGui::ShowDemoWindow(NULL);

        ImGui::Render();
    }

    fmt::print("DestroyContext()\n");
    ImGui::DestroyContext();

    return 0;
}
