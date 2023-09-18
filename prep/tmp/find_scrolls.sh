#!/usr/bin/env bash

SOURCES=(
    "../../../Source/Shared_PAK/Public/Shared/Stats/Generated/Data/Object.txt"
    "../../../Source/Shared_PAK/Public/SharedDev/Stats/Generated/Data/Object.txt"
    "../../../Source/Gustav_PAK/Public/Gustav/Stats/Generated/Data/Object.txt"
    "../../../Source/Gustav_PAK/Public/GustavDev/Stats/Generated/Data/Object.txt"
    "../../SecretScrolls5eSpells/PAK/Public/SecretScrolls5eSpells/Stats/Generated/Data/Object_SecretScrolls5eSpells.txt"
)

SCROLLS_TMP="Scrolls.tmp"
SCROLLS_FILE="Scrolls.txt"

echo "" > "${SCROLLS_TMP}"
for SOURCE in "${SOURCES[@]}"; do
    grep OBJ_Scroll_ "${SOURCE}" | awk '{ print $3 }' | tr -d '"' >> "${SCROLLS_TMP}"
done

egrep -v '^$' "${SCROLLS_TMP}" | sort > "${SCROLLS_FILE}"
rm "${SCROLLS_TMP}"
