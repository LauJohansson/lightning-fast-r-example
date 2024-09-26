# Databricks notebook source
# MAGIC %md
# MAGIC ## Installing R packages

# COMMAND ----------

# MAGIC %md
# MAGIC ## Introduction
# MAGIC
# MAGIC This notebook installs the required R libraries.
# MAGIC
# MAGIC The libraries gets installed into `/usr/lib/R/site-library`
# MAGIC
# MAGIC Afterwards, the libraries gets copied into `dbfs:/FileStore/Rpackage/rlibrary`
# MAGIC
# MAGIC The libraries can then be easily applied in other notebooks by running: `%r .libPaths(c(.libPaths(), normalizePath("/dbfs/FileStore/Rpackage/rlibrary/")))`

# COMMAND ----------

# MAGIC %md
# MAGIC ## Install libaries

# COMMAND ----------

# ruff: noqa: E501

# COMMAND ----------

import os
import sys

sys.path.append(os.path.abspath(".."))
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
dbutils = w.dbutils

# COMMAND ----------

from typing import List


def check_libraries_exists_usr(expected_libraries: List[str], dbutils) -> None:
    """
    Checks if the expected R libraries exist in the local
    `/usr/lib/R/site-library` path.

    Args:
        expected_libraries (List[str]): A list of R library names to check.
        dbutils: Databricks utility object used to interact with the filesystem.

    Raises:
        Exception: If the subfolder for any library is not found in the specified path.
    """
    for library in expected_libraries:
        library_path = f"file:/usr/lib/R/site-library/{library}"
        try:
            if not any(dbutils.fs.ls(library_path)):
                raise Exception(
                    f"Subfolder for library {library} "
                    f"not found in file:/usr/lib/R/site-library"
                )
        except:  # noqa: E722
            raise Exception(
                f"Subfolder for library {library} "
                f"not found in file:/usr/lib/R/site-library"
            )


def check_libraries_exists_filestorage(expected_libraries: List[str], dbutils) -> None:
    """
    Checks if the expected R libraries exist
    in the Databricks FileStore path `/FileStore/Rpackage/rlibrary`.

    Args:
        expected_libraries (List[str]): A list of R library names to check.
        dbutils: Databricks utility object used to interact with the filesystem.

    Raises:
        Exception: If the subfolder for any library is not found in the specified path.
    """
    for library in expected_libraries:
        library_path = f"dbfs:/FileStore/Rpackage/rlibrary/{library}"
        try:
            if not any(dbutils.fs.ls(library_path)):
                raise Exception(
                    f"Subfolder for library {library} "
                    f"not found in dbfs:/FileStore/Rpackage/rlibrary"
                )
        except:  # noqa: E722
            raise Exception(
                f"Subfolder for library {library} "
                f"not found in dbfs:/FileStore/Rpackage/rlibrary"
            )


# COMMAND ----------

# MAGIC %r
# MAGIC # Define a dictionary with package names and versions
# MAGIC packages <- list(
# MAGIC   "ggplot2" = "3.5.1",
# MAGIC   "reshape" = "0.8.9",
# MAGIC )
# MAGIC
# MAGIC # Loop through the dictionary and install each package
# MAGIC for (pkg in names(packages)) {
# MAGIC   version <- packages[[pkg]]
# MAGIC   url <- paste0("https://cran.r-project.org/package=", pkg, "&version=", version)
# MAGIC   cat("Installing package:", pkg, "version:", version, "\n")
# MAGIC   cat("======================================\n")
# MAGIC   utils::install.packages(pkgs = url, repos = NULL, lib="/usr/lib/R/site-library")
# MAGIC }
# MAGIC

# COMMAND ----------

# MAGIC %r
# MAGIC path <-"/dbfs/FileStore/<your-package>.tar.gz"
# MAGIC install.packages(pkgs=path, repos = NULL, type="source", lib="/usr/lib/R/site-library")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Ensure libaries are installed in file:/usr/lib/R/site-library

# COMMAND ----------

if not any(dbutils.fs.ls("file:/usr/lib/R/site-library")):
    raise Exception("Nothing to be found in file:/usr/lib/R/site-library")

# COMMAND ----------

expected_libraries = [
    "ggplot2",
    "reshape",
    "YourPackage",
]

# COMMAND ----------


# Check if each element in expected_libraries has a corresponding subfolder in the directory
check_libraries_exists_usr(expected_libraries, dbutils)

# COMMAND ----------

# MAGIC %md
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Clear dbfs R packages

# COMMAND ----------

# Clear the library
dbutils.fs.rm("dbfs:/FileStore/Rpackage/rlibrary", True)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Copy R packages to DBFS

# COMMAND ----------

# Specify the source local path
local_source = "file:/usr/lib/R/site-library"

# Specify the destination DBFS location
dbfs_destination = "dbfs:/FileStore/Rpackage/rlibrary"

# Copy files and folders from local path to DBFS
dbutils.fs.cp(local_source, dbfs_destination, recurse=True)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Ensure libaries are installed in dbfs:/FileStore/Rpackage/rlibrary

# COMMAND ----------

if not any(dbutils.fs.ls("dbfs:/FileStore/Rpackage/rlibrary")):
    raise Exception("Nothing to be found in dbfs:/FileStore/Rpackage/rlibrary")

# COMMAND ----------

check_libraries_exists_filestorage(expected_libraries, dbutils)
