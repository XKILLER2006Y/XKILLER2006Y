#
# Vendorsetup Shell Script for Universal Recovery Workspace
#

# Export RamaBP Advanced OrangeFox Environment Flags
export OF_STATUS_H=95
export OF_ENABLE_LPTOOLS=1
export OF_DEFAULT_KEYMASTER_VERSION=4.1
export OF_UNBIND_SDCARD_F2FS=1
export OF_WIPE_METADATA_AFTER_DATAFORMAT=1
export OF_BIND_MOUNT_SDCARD_ON_FORMAT=1
export OF_ENABLE_ALL_PARTITION_TOOLS=1
export FOX_VIRTUAL_AB_DEVICE=1
export FOX_VANILLA_BUILD=1
export FOX_ENABLE_APP_MANAGER=1
export FOX_RECOVERY_SYSTEM_PARTITION="/dev/block/mapper/system"
export FOX_RECOVERY_VENDOR_PARTITION="/dev/block/mapper/vendor"
export FOX_USE_BASH_SHELL=1
export FOX_ASH_IS_BASH=1
export FOX_USE_LZ4_BINARY=1
export FOX_USE_ZSTD_BINARY=1
export FOX_DELETE_AROMAFM=1

# Legacy lunch combo registration (compatibility with older build systems)
if type add_lunch_combo > /dev/null 2>&1; then
    add_lunch_combo twrp_X6871-userdebug
    add_lunch_combo fox_X6871-userdebug
    add_lunch_combo pbrp_X6871-userdebug
    add_lunch_combo shrp_X6871-userdebug
    add_lunch_combo lineage_X6871-userdebug
    add_lunch_combo aosp_X6871-userdebug
    add_lunch_combo omni_X6871-userdebug
fi
