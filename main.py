#IOMMU Installer for Arch Linux , Identicial Graphics Cards

import fileinput
import re
import sys
import os
from sys import platform
print("Enter intel or amd depending on your cpu make")
cpu = input("Please enter your cpu brand:")
file_name = 'examplegrub' #this will be /etc/default/grub once deployed
if cpu == "amd":
    iommu_type = '"amd_iommu=on iommu=pt '
elif cpu == "intel":
    iommu_type = '"intel_iommu=on iommu=pt '
#Opens grub file, puts each line into an array
with open('examplegrub') as grubfile:
    grubline = [i.strip() for i in grubfile]
#looping through array
for y in grubline:
    #matching needed line with looped array
    x = re.search('^GRUB_CMDLINE_LINUX_DEFAULT=".*"', y)
    if x:
        #if syntax is correct then stored needed string in editedgrub
        print("Edited grubline")
        #replace each '"' occurance in grubline array with iommu
        editedgrub = re.sub('"', iommu_type, y, 1)
        print(editedgrub)
        for line in fileinput.FileInput('examplegrub', inplace=1):
            line=line.replace(y, editedgrub)
            print(line.strip())
system = input("please enter your system (linux/arch)")
#updating grub (sudo user)
grubupdate = 'sudo update-grub'
#kernal modules
vfio = ' vfio_pci vfio vfio_iommu_type1 vfio_virqfd '
#cross compatibility (eventually)
if system == "linux":
    os.system(grubupdate)
    print("work in progress")
if system == "arch":
    os.system(grubupdate)
    #opening kernal configuration
    with open('mkinitcpio.conf') as loadfile:
        kernal_changes = [p.strip() for p in loadfile]
        for it in kernal_changes:
            n = re.search('^MODULES=(.*)$', it)
            if n: #if n is true after re.search then add modules
                print("Editing kernal modules")
                kernal_modules = re.sub('\s', vfio, it, 1)
                print(kernal_modules)
                for kernal_line in fileinput.FileInput('mkinitcpio.conf', inplace=1):
                    kernal_line=kernal_line.replace(it, kernal_modules)
                    print("Edited configurations")
                    print(kernal_line.strip())
                    print(line.strip())
    with open('mkinitcpio.conf') as hookfile:
        hook_changes = [z.strip() for z in hookfile]
        for hook in hook_changes:
            new_hook = 'modconf'
            h = re.search('^HOOKS=(.*)$', hook)
            if h:
                print("Editing Hooks")
                hook_edit = re.sub('\s', new_hook, h, 1)
                print(hook_edit) #currently broken
                for hook_line in fileinput.FileInput('mkinitcpio.conf', inplace=1):
                    hook_line=hook_line.replace(h, hook_changes)
                    print("Edited configurations")
                    print(hook_line.strip())
                    print(line.strip())

