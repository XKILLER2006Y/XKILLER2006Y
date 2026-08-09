#
# Product Target Makefile for OmniROM Fallback Target
# Device: Infinix GT 20 Pro (X6871)
#

$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)
$(call inherit-product, device/infinix/X6871/device.mk)

PRODUCT_NAME := omni_X6871
PRODUCT_DEVICE := X6871
PRODUCT_BRAND := Infinix
PRODUCT_MODEL := Infinix GT 20 Pro
PRODUCT_MANUFACTURER := INFINIX

# Verified GKI v4 Target
