# Universal Recovery Device Tree for Infinix GT 20 Pro (X6871)

[![Platform](https://img.shields.io/badge/Platform-MediaTek%20MT6896%20%2F%20Dimensity%208200%20Ultimate-orange.svg)](https://www.mediatek.com/)
[![Architecture](https://img.shields.io/badge/Architecture-arm64--v8a-blue.svg)](https://developer.arm.com/)
[![Recovery Frameworks](https://img.shields.io/badge/Recovery-TWRP%20%7C%20OrangeFox%20%7C%20PBRP%20%7C%20SHRP%20%7C%20Lineage-green.svg)](https://twrp.me/)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-Automated%20Cloud%20Build-blueviolet.svg)](https://github.com/features/actions)

Unified, production-grade custom recovery device tree for compiling **TWRP**, **OrangeFox Recovery**, **PitchBlack (PBRP)**, **SkyHawk (SHRP)**, **Lineage Recovery**, or **AOSP Recovery** for the **Infinix GT 20 Pro (`X6871`)**, powered by MediaTek Dimensity 8200 Ultimate (`MT6896`).

---

## Supported Recovery Framework Matrix

| Recovery Engine | Target Makefile | Lunch Target | Output Partition | Status |
| :--- | :--- | :--- | :--- | :---: |
| **TWRP (11 / 12 / 12.1)** | `twrp_X6871.mk` | `twrp_X6871-userdebug` | `vendor_boot` | **READY** |
| **OrangeFox Recovery (R11 / R12)** | `fox_X6871.mk` | `fox_X6871-userdebug` | `vendor_boot` | **READY** |
| **PitchBlack Recovery (PBRP)** | `pbrp_X6871.mk` | `pbrp_X6871-userdebug` | `vendor_boot` | **READY** |
| **SkyHawk Recovery (SHRP)** | `shrp_X6871.mk` | `shrp_X6871-userdebug` | `vendor_boot` | **READY** |
| **Lineage Recovery** | `lineage_X6871.mk` | `lineage_X6871-userdebug` | `vendor_boot` | **READY** |
| **AOSP Recovery** | `aosp_X6871.mk` | `aosp_X6871-userdebug` | `vendor_boot` | **READY** |

---

## Directory Structure

```
device/infinix/X6871/
├── .github/
│   └── workflows/
│       └── build_recovery.yml          # GitHub Actions Automated Cloud Compiler
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
├── README.md                            # GitHub repository front page
└── prebuilt/
    └── dtb                              # Official stock MediaTek MT6896 kernel DTB (318,821 bytes)
```

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

## Compiling locally on Linux

```bash
# Set up workspace & clone tree
mkdir -p ~/recovery && cd ~/recovery
repo init -u https://gitlab.com/OrangeFox/Manifest.git -b fox_12.1
repo sync -c -j$(nproc --all)

mkdir -p device/infinix/X6871
git clone https://github.com/YOUR_USERNAME/android_device_infinix_X6871.git device/infinix/X6871

# Build OrangeFox
source build/envsetup.sh
lunch fox_X6871-userdebug
mka recoveryimage -j$(nproc --all)
```

---

## Flashing Instructions

```bash
fastboot flash vendor_boot out/target/product/X6871/vendor_boot.img
fastboot reboot recovery
```
