#
# Copyright (C) 2026 Universal Recovery Project
# Production Device Make File for Infinix GT 20 Pro (X6871)
#

LOCAL_PATH := $(call my-dir)

# Inherit virtual A/B configuration
$(call inherit-product, $(SRC_TARGET_DIR)/product/virtual_ab_ota.mk)

# Device Identifiers & Platform
PRODUCT_BRAND := Infinix
PRODUCT_MODEL := Infinix GT 20 Pro
PRODUCT_DEVICE := X6871
PRODUCT_MANUFACTURER := INFINIX
PRODUCT_PLATFORM := mt6896

# Enable Virtual A/B & Dynamic Partitions
PRODUCT_VIRTUAL_AB_OTA := true
PRODUCT_BUILD_SUPER_PARTITION := true
PRODUCT_USE_DYNAMIC_PARTITIONS := true

# Display, Density & API Levels
PRODUCT_SHIPPING_API_LEVEL := 31
PRODUCT_PROPERTY_OVERRIDES += \
    ro.sf.lcd_density=480 \
    ro.recovery.ui.margin_height=126

# Init Scripts Installation
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/recovery/root/init.recovery.mt6895.rc:$(TARGET_COPY_OUT_RECOVERY)/root/init.recovery.mt6895.rc \
    $(LOCAL_PATH)/recovery/root/init.recovery.mt6896.rc:$(TARGET_COPY_OUT_RECOVERY)/root/init.recovery.mt6896.rc \
    $(LOCAL_PATH)/recovery/root/init.recovery.usb.rc:$(TARGET_COPY_OUT_RECOVERY)/root/init.recovery.usb.rc
