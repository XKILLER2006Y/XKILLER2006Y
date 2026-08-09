#
# Product Target Makefile for OrangeFox Recovery R11 / R12
# Device: Infinix GT 20 Pro (X6871)
#

$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)
$(call inherit-product, device/infinix/X6871/device.mk)

PRODUCT_NAME := fox_X6871
PRODUCT_DEVICE := X6871
PRODUCT_BRAND := Infinix
PRODUCT_MODEL := Infinix GT 20 Pro
PRODUCT_MANUFACTURER := INFINIX

# RamaBP Advanced OrangeFox Flags
OF_STATUS_H := 95
OF_ENABLE_LPTOOLS := 1
OF_DEFAULT_KEYMASTER_VERSION := 4.1
OF_UNBIND_SDCARD_F2FS := 1
OF_WIPE_METADATA_AFTER_DATAFORMAT := 1
OF_BIND_MOUNT_SDCARD_ON_FORMAT := 1
OF_ENABLE_ALL_PARTITION_TOOLS := 1
FOX_VIRTUAL_AB_DEVICE := 1
FOX_VANILLA_BUILD := 1

# Verified GKI v4 Target
