#
# Copyright (C) 2026 Universal Recovery Project
# Product Definitions for TWRP, OrangeFox, PBRP, SHRP, Lineage Recovery & AOSP Recovery
#

PRODUCT_MAKEFILES := \
    $(LOCAL_DIR)/twrp_X6871.mk \
    $(LOCAL_DIR)/fox_X6871.mk \
    $(LOCAL_DIR)/pbrp_X6871.mk \
    $(LOCAL_DIR)/shrp_X6871.mk \
    $(LOCAL_DIR)/lineage_X6871.mk \
    $(LOCAL_DIR)/aosp_X6871.mk \
    $(LOCAL_DIR)/omni_X6871.mk

COMMON_LUNCH_CHOICES := \
    twrp_X6871-userdebug \
    fox_X6871-userdebug \
    pbrp_X6871-userdebug \
    shrp_X6871-userdebug \
    lineage_X6871-userdebug \
    aosp_X6871-userdebug \
    omni_X6871-userdebug

# Verified GKI v4 Target
