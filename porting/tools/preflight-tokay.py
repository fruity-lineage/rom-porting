#!/usr/bin/env python3
"""Run the ROM static preflight with Tokay lists and distinct recovery manifests."""
import importlib.util
import sys
from pathlib import Path

SKILL_SCRIPTS = Path('/serverhive4/fruitzail/.agents/skills/reverse-engineering-cherry-picking/scripts')
sys.path.insert(0, str(SKILL_SCRIPTS))
SPEC = importlib.util.spec_from_file_location('rom_preflight', SKILL_SCRIPTS / 'preflight.py')
PREFLIGHT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREFLIGHT)

CHECK_LISTS = PREFLIGHT.check_lists
CHECK_VINTF = PREFLIGHT.check_vintf


def check_lists(device_tree, vendor):
    CHECK_LISTS(str(Path(device_tree) / 'tokay'), vendor)


def check_vintf(sources):
    normal = [(path, text) for path, text in sources if '/recovery/' not in path]
    recovery = [(path, text) for path, text in sources if '/recovery/' in path]
    print(f'VINTF: {len(normal)} normal manifests, {len(recovery)} recovery manifests')
    CHECK_VINTF(normal)
    CHECK_VINTF(recovery)


if __name__ == '__main__':
    PREFLIGHT.check_lists = check_lists
    PREFLIGHT.check_vintf = check_vintf
    sys.argv = [sys.argv[0], '--dt', 'device/google/caimito',
                '--hw', 'device/google/zumapro', '--vendor-dir', 'vendor/google/tokay',
                '--module-dir', 'hardware/google/pixel', '--module-dir', 'system/core/trusty',
                '--module-dir', 'frameworks/base/services/duck_rkp',
                '--module-dir', 'vendor/lineage', '--module-dir', 'device/lineage/sepolicy']
    PREFLIGHT.main()
