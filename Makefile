obj-m	:= src/facer.o

KERNELDIR ?= /lib/modules/$(shell uname -r)/build
PWD       := $(shell pwd)

# Warning level (W=1..3). Change to taste at invoke-time: `make W=2`
W ?= 1


# Sign the kernel module for secure boot (Ubuntu)
# https://wiki.ubuntu.com/UEFI/SecureBoot/Signing
KEY := /var/lib/shim-signed/mok/MOK.priv
X509 := /var/lib/shim-signed/mok/MOK.der

ifdef LTS
    ccflags-y := -Dlts
endif

# Apply strong warnings to *all subdirs* (like src/)
# Keep it readable; you can tune if any are too chatty.
subdir-ccflags-y += -Wall -Wextra -Wformat=2 -Werror \
                    -Wstringop-overflow=4 -Wstringop-truncation \
                    -Wvla -Wimplicit-fallthrough=5 -Wcast-function-type \
                    -Wno-missing-field-initializers -fno-common

all: default

default:
	$(MAKE) -C $(KERNELDIR) M=$(PWD) W=$(W) modules

#	if [ -f "$(KEY)" ] && [ -f "$(X509)" ]; then \
#		sudo kmodsign sha512 $(KEY) $(X509) src/facer.ko; \
#	fi

install:
	$(MAKE) -C $(KERNELDIR) M=$(PWD) modules_install

clean:
	rm -rf src/*.o src/*~ src/.*.cmd src/*.ko src/*.mod.c \
		.tmp_versions modules.order Module.symvers

dkmsclean:
	@dkms remove facer/0.1 --all || true
	@dkms remove facer/0.2 --all || true

dkms: dkmsclean
	dkms add .
	dkms install -m facer -v 0.2

onboot:
	echo "facer" > /etc/modules-load.d/facer.conf

noboot:
	rm -f /etc/modules-load.d/facer.conf
	
	

.PHONY: default all clean install dkms dkmsclean onboot noboot lint clang

# Static analysis helpers (optional but recommended)
lint:
	# Sparse (C=2 gives more checks). Requires 'sparse' installed.
	$(MAKE) -C $(KERNELDIR) M=$(PWD) C=2 CHECK=sparse W=$(W) modules

clang:
	# Try a Clang build; catches different UB than GCC.
	$(MAKE) -C $(KERNELDIR) M=$(PWD) CC=clang LLVM=1 W=$(W) modules
