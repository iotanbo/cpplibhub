# Zen of cpplibhub


### Things must be as simple as possible, but not simpler

This famous Einstein advice is indispensable. `cpplibhub` is trying to keep balance between too complex and too simple.

### Flat is better than nested

This is an important point from Zen of Python that applies to `cpplibhub` as well. Deep nesting begets a lot of problems, like more complex dependency graphs and redundancy in disk storage usage if same modules are present more than once on different hierarchy level.

### User experience matters

This tool is made for programmers to help them concentrate on code, not on chores that make it running. It allows them to be more creative, positive and productive.


# How it works

### Basic ideas

#### Single place for C/C++ libraries on the disk


#### Reduced redundancy

Modules that can be shared between projects, must be shared.

#### Mess up with system libraries as little as possible


#### Simple `cmake` files make them attractive to users.


## Directory structure

```
cpplibhub # home directory for all libraries and projects
│
├─ DEV 	# libraries that are in development; may be a root for IDE like CLion
│	│
│  	└─ mylib@iotanbo  # project roots
│		│
│		├─ common  # files that are common for all configurations
│		│	├─  v1.0.1  # version
│		│	└─  v1.2.1  # another version
│		│
│    	└─ lib  # compiled libraries will be located heresssssssss
│			└─ v1.0.1    # version
│					└─ linux  # target platform
│							└─ amd64  # target arch
│								└─ gcc9  # compiler set name
│									└─ rel  # configuration
│										└─ static  # link type

```



## Examples

### Project files

####  mylib.cpplibhub


```
# Dependency file example for mylib

description="""
...Here goes library description.
"""

# Common prerequisites for all types of host platforms
common_for_all_host_platforms:

tools: # Tools and other stuff required to build mylib

end_tools;

conditions:  # Conditions that must be satisfied
# Each condition has a predefined python class and
# standard calling scheme
end_conditions;

libs:  # Libraries that must be present

end_libs;

end_common_for_all_host_platforms;  # Section end

# Common prerequisites for all types of target platforms
common_for_all_target_platforms:

end_host_os_common;

target_os: android, ios  # Prerequisites for android and ios only

end_common_for_all_target_platforms;



```


### Terminology

**host platform** - platform on which the build is done. Major desktop platforms: windows, linux, macos.

**target platform** - platform the code is intended for. Example: windows, linux, macos, android, ios.

