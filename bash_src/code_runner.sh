#!/bin/bash

filename=$1
debug=0
cpp_version="c++17"

if [[ $filename == *.c ]]; then
  extension=".c"
  compiler="gcc"
  language="c"
elif [[ $filename == *.cpp ]]; then
  extension=".cpp"
  compiler="g++"
  language="c++"
elif [[ $filename == *.java ]]; then
  extension=".java"
  compiler="javac"
  language="java"
elif [[ $filename == *.go ]]; then
  extension=".go"
  compiler="go run"
  language="go"
elif [[ $filename == *.cs ]]; then
  extension=".cs"
  compiler="csc"
  language="csharp"
elif [[ $filename == *.swift ]]; then
  extension=".swift"
  compiler="swift"
  language="swift"
# add for python
elif [[ $filename == *.py ]]; then
  extension=".py"
  compiler="python3"
  language="python"
elif [[ $filename == *.js ]]; then
  extension=".js"
  compiler="node"
  language="javascript"
elif [[ $filename == *.rs ]]; then
  extension=".rs"
  compiler="rustc"
  language="rust"
else
  echo "Error: Unsupported file type"
  exit 1
fi

if [ $language == "c++" ]; then
  if [[ $3 == c++* ]]; then
    version=${3#c++}
    if [[ $version == 17 || $version == 14 || $version == 11 || $version == 0x ]]; then
      cpp_version="c++$version"
    fi
  fi
fi

if [[ $2 == "--debug" ]]; then
  debug=1
fi

if [ $debug -eq 1 ]; then
  if [ $language == "c++" ]; then
    echo "Compiling $filename with $compiler (C++ $cpp_version)..."
  else
    echo "Compiling $filename with $compiler..."
  fi
fi

if [ $language == "c" ]; then
  $compiler $filename -o ${filename%.*}
elif [ $language == "c++" ]; then
  $compiler $filename -std=$cpp_version -o ${filename%.*}
elif [ $language == "java" ]; then
  $compiler $filename
elif [ $language == "go" ]; then
  $compiler $filename
elif [ $language == "csharp" ]; then
  $compiler /out:${filename%.*}.exe $filename
elif [ $language == "swift" ]; then
  $compiler $filename
elif [ $language == "python" ]; then
  $compiler $filename
elif [ $language == "javascript" ]; then
  $compiler $filename
elif [ $language == "rust" ]; then
  $compiler $filename
else
  echo "Error: Unsupported file type"
  exit 1
fi

if [ $? -ne 0 ]; then
  echo "Compilation failed"
  exit 1
fi

if [ $debug -eq 1 ]; then
  echo "Running ${filename%.*}..."
fi

if [ $language == "java" ]; then
  java ${filename%.*}
elif [ $language == "go" ]; then
  $compiler $filename
else
  ./${filename%.*}
fi

if [ $debug -eq 1 ]; then
  echo "Finished running ${filename%.*}"
fi

