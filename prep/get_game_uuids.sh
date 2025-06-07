#!/usr/bin/env bash

grep -A3 OBJ_Scroll source_objects/Shared/Object.txt  | egrep -w '(new entry|RootTemplate)' > source_objects/compiled.txt

grep -A3 OBJ_Scroll source_objects/SharedDev/Object.txt  | egrep -w '(new entry|RootTemplate)' >> source_objects/compiled.txt

sed -En 's/^(new entry "[^"]+"|data "RootTemplate" "[^"]+"|^$)/\1/p' source_objects/compiled.txt | tr -d '"' | awk '{ print $NF }' | egrep '^[a-z0-9]' | sed 's/\(.*\)/"\1",/'