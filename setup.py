# Packages an already-compiled OCP extension module (built via CMake/Ninja,
# not via this setup.py) into a wheel. The CI workflow stages the compiled
# module and its stub package into ./wheel_staging/ before invoking this.
#
# Keep VERSION in sync with conda/meta.yaml's OCCT_VER.OCP_TWEAK.
import glob
import os

from setuptools import setup
from setuptools.dist import Distribution

VERSION = "8.0.0.0"

STAGING_DIR = "wheel_staging"


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True


def find_staged_files():
    files = []
    for root, _dirs, names in os.walk(STAGING_DIR):
        for name in names:
            files.append(os.path.relpath(os.path.join(root, name), STAGING_DIR))
    return files


setup(
    name="OCP",
    version=VERSION,
    description="Python bindings for OCCT (pybind11)",
    package_dir={"": STAGING_DIR},
    packages=[""],
    package_data={"": find_staged_files()},
    include_package_data=True,
    distclass=BinaryDistribution,
    zip_safe=False,
)
