# Universal Recovery Device Tree for Infinix GT 20 Pro (X6871)

[![Platform](https://img.shields.io/badge/Platform-MediaTek%20MT6896%20%2F%20Dimensity%208200%20Ultimate-orange.svg)](https://www.mediatek.com/)
[![Architecture](https://img.shields.io/badge/Architecture-arm64--v8a-blue.svg)](https://developer.arm.com/)
[![Recovery Frameworks](https://img.shields.io/badge/Recovery-TWRP%20%7C%20OrangeFox%20%7C%20PBRP%20%7C%20SHRP%20%7C%20Lineage-green.svg)](https://twrp.me/)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-Automated%20Cloud%20Build-blueviolet.svg)](https://github.com/features/actions)

Unified, production-grade custom recovery device tree for compiling **TWRP**, **OrangeFox Recovery**, **PitchBlack (PBRP)**, **SkyHawk (SHRP)**, **Lineage Recovery**, or **AOSP Recovery** for the **Infinix GT 20 Pro (`X6871`)**, powered by MediaTek Dimensity 8200 Ultimate (`MT6896`).

---

## Supported Recovery Framework Matrix

| Recovery Engine | Target Makefile | Lunch Target | Output Partition | Default Branch | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TWRP (11 / 12 / 12.1)** | `twrp_X6871.mk` | `twrp_X6871-userdebug` | `vendor_boot` | `twrp-12.1` | **READY** |
| **OrangeFox Recovery (R11 / R12)** | `fox_X6871.mk` | `fox_X6871-userdebug` | `vendor_boot` | `fox_12.1` | **READY** |
| **PitchBlack Recovery (PBRP)** | `pbrp_X6871.mk` | `pbrp_X6871-userdebug` | `vendor_boot` | `android-12.1` | **READY** |
| **SkyHawk Recovery (SHRP)** | `shrp_X6871.mk` | `shrp_X6871-userdebug` | `vendor_boot` | `twrp-12.1` | **READY** |
| **Lineage Recovery** | `lineage_X6871.mk` | `lineage_X6871-userdebug` | `vendor_boot` | `lineage-21.0` | **READY** |
| **AOSP Recovery** | `aosp_X6871.mk` | `aosp_X6871-userdebug` | `vendor_boot` | `twrp-12.1` | **READY** |

---

## Directory Structure

```
device/infinix/X6871/
├── .github/
│   └── workflows/
│       └── build_recovery.yml          # GitHub Actions Automated Cloud Compiler (40GB+ Free Disk, ccache)
├── Android.mk                           # Top-level makefile entry
├── AndroidProducts.mk                   # Product registry for all recovery engines
├── BoardConfig.mk                       # Unified hardware platform & super partition math
├── device.mk                            # Product flags, API levels, copy rules
├── twrp_X6871.mk                        # TWRP build target
├── fox_X6871.mk                         # OrangeFox build target
├── pbrp_X6871.mk                        # PitchBlack PBRP build target
├── shrp_X6871.mk                        # SkyHawk SHRP build target
├── lineage_X6871.mk                     # Lineage Recovery build target
├── aosp_X6871.mk                        # AOSP Recovery build target
├── omni_X6871.mk                        # OmniROM fallback build target
├── vendorsetup.sh                       # Lunch combo generator
├── recovery.fstab                       # FBE v2, EROFS, EXT4, F2FS partition table
├── twrp.flags                           # TWRP/Fox graphical partition routes & removable drives
├── system.prop                          # Recovery hardware & USB controller properties
├── README.md                            # GitHub repository documentation
└── prebuilt/
    └── dtb                              # Official stock MediaTek MT6896 kernel DTB (318,821 bytes)
```

---

## GitHub Actions Automated Cloud Build

The repository includes a GitHub Actions workflow (`.github/workflows/build_recovery.yml`) supporting manual dispatch (`workflow_dispatch`).

### Features:
1. **Clean UI Modal Input**: `MANIFEST_BRANCH` can be left blank; the workflow automatically detects and selects the ideal branch for your selected engine (`fox_12.1`, `twrp-12.1`, `pb-12.1`, `shrp-12.1`, `lineage-19.1`).
2. **Reclaim 40+ GB Disk Space**: Automatically strips unnecessary runner packages (Android SDK, Dotnet, Haskell, Docker caches) before repo sync.
3. **Persistent ccache**: Speeds up repeated runs by caching compilation objects across workflow dispatches (`~/.ccache`).
4. **Clean Artifact Output**: Safely staging and uploading built images (`vendor_boot.img`, `recovery.img`, `.zip`) with artifact compression.

---

## How to Push to GitHub

To publish this tree to GitHub:

```bash
# Navigate to device tree directory
cd device/infinix/X6871

# Initialize git & push to GitHub
git init
git add .
git commit -m "Initial commit: Universal Recovery Device Tree for Infinix GT 20 Pro (X6871)"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/android_device_infinix_X6871.git
git push -u origin main
```

---

## Compiling Locally on Linux

```bash
# Set up workspace & clone tree
mkdir -p ~/recovery && cd ~/recovery
repo init -u https://gitlab.com/OrangeFox/Manifest.git -b fox_12.1 --depth=1
repo sync -c -j$(nproc --all)

mkdir -p device/infinix/X6871
git clone https://github.com/YOUR_USERNAME/android_device_infinix_X6871.git device/infinix/X6871

# Build OrangeFox
source build/envsetup.sh
lunch fox_X6871-userdebug
mka recoveryimage vendorbootimage -j$(nproc --all)
```

---

## Flashing Instructions

```bash
fastboot flash vendor_boot out/target/product/X6871/vendor_boot.img
fastboot reboot recovery
```
