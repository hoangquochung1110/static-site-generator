# Archiving and Compressing in Linux


## tar
- To archive
```
$tar -cvf archive_name.tar [files | directories]
```

Breakdown:
* -c: This option stands for create. It tells tar to create a new archive.
* -v: This option stands for verbose. It instructs tar to display detailed output during the archiving process, showing the names of the files being added to the archive.
* -f: This option stands for file. It indicates that the next argument will be the name of the archive file to be created. This is necessary because tar can work with multiple types of input and output.

- To extract:
```
$tar -xvf archive.tar

$tar -xvf archive.tar -C /path/to/directory/
```

Breakdown:
* -x: This option stands for extract. It tells tar to extract files from the specified archive.
* -C: Extracting the files to a Specific Directory


## Compressing

| Command                   | Description                                               | Example Usage                                  |
|---------------------------|-----------------------------------------------------------|------------------------------------------------|
| `gzip`                    | Compress a file using gzip                                 | `gzip filename`                                |
| `gunzip`                  | Decompress a gzip file                                    | `gunzip filename.gz`                           |
| `bzip2`                   | Compress a file using bzip2                               | `bzip2 filename`                               |
| `bunzip2`                 | Decompress a bzip2 file                                   | `bunzip2 filename.bz2`                         |
| `zip`                     | Create a zip archive                                      | `zip archive.zip file1 file2`                 |
| `unzip`                   | Extract files from a zip archive                          | `unzip archive.zip`                            |
| `xz`                      | Compress a file using xz                                   | `xz filename`                                  |
| `unxz`                    | Decompress an xz file                                     | `unxz filename.xz`                            |


## tar + compression: can compress and decompress using other tools
| Command                   | Description
|---------------------------|------------------------------------------------------------------
| `tar -czf file.tgz`       | create a compressed archive with the **gzip** compression algorithm
| `tar -xjf file.tbz`       | Extract files from a compressed tar archive with the **bunzip** compressing algorithm
| `tar -xJf file.txz`       | Extract files from a compressed tar archive with the **xz** compressing algorithm
