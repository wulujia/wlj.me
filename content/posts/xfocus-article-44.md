---
title: "GCC使用指南"
date: 2000-06-08T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-44"
---

(quack_at_xfocus.org)

GCC使用指南


使用语法： 

       gcc [ option | filename ]... 

       g++ [ option | filename ]... 

 

       其中 option   为 gcc 使用时的选项(后面会再详述)， 

         而 filename 为欲以 gcc 处理的文件 

说明： 

      这 C 与 C++ 的 compiler 已将产生新程序的相关程序整合起来。产 

      生一个新的程序需要经过四个阶段：预处理、编译、汇编,连结， 

      而这两个编译器都能将输入的文件做不同阶段的处理。虽然原始程序 

     的扩展名可用来分辨编写原始程序码所用的语言，但不同的 compiler 

      ，其预设的处理程序却各不相同： 

 

       gcc    预设经由预处理过(扩展名为.i)的文件为 C 语言，并於程 

              式连结阶段以 C 的连结方式处理。 

 

       g++    预设经由预处理过(扩展名为.i)的文件为 C++ 语言，并於程


序连结阶段以 C++ 的连结方式处理。 

 

 

       原始程序码的扩展名指出所用编写程序所用的语言，以及相对应的处 

       理方法： 

 

       .c    C 原始程序                     ；   预处理、编译、汇编 

       .C    C++ 原始程序                   ；   预处理、编译、汇编 

       .cc   C++ 原始程序                   ；   预处理、编译、汇编 

       .cxx  C++ 原始程序                   ；   预处理、编译、汇编 

       .m    Objective-C 原始程序           ；   预处理、编译、汇编 

       .i    已经过预处理之 C 原始程序    ；   编译、汇编 

       .ii   已经过预处理之 C++ 原始程序  ；   编译、汇编 

       .s    组合语言原始程序               ；   汇编 

       .S    组合语言原始程序               ；   预处理、汇编 

       .h    预处理文件(标头文件)           ；   (不常出现在指令行) 

 

 

       其他扩展名的文件是由连结程序来处理，通常有： 

 

       .o    Object file 

       .a    Archive file 

 

 

       除非编译过程出现错误，否则 "连结" 一定是产生一个新程序的最 

       後阶段。然而你也可以以 -c、-s 或 -E 等选项，将整个过程自四 

       个阶段中的其中一个停止。在连结阶段，所有与原始码相对应的 

       .o 文件、程序库、和其他无法自文件名辨明属性的文件(包括不以 .o 

       为扩展名的 object file 以及扩展名为 .a 的 archive file)都会 

       交由连结程序来处理(在指令行将那些文件当作连结程序的参数传给 

       连结程序)。 

 

 

选项： 

       不同的选项必须分开来下：例如 `-dr' 这个选项就与 `-d -r' 大 

       不相同。 

 

       绝大部份的 `-f' 及 `-W' 选项都有正反两种形式：-fname 及 

       -fno-name (或 -Wname 及 -Wno-name)。以下只列出非预设的那个 

       形式。 

 

       以下是所有选项的摘要。以形式来分类。选项的意义将另辟小节说 

       明。 

 

       一般性(概略、常用的)选项 

              -c -S -E -o file -pipe -v -x language 

 

       程序语言选项 

              -ansi -fall-virtual -fcond-mismatch 

              -fdollars-in-identifiers -fenum-int-equiv 

              -fexternal-templates -fno-asm -fno-builtin 

              -fno-strict-prototype -fsigned-bitfields 

              -fsigned-char -fthis-is-variable 

              -funsigned-bitfields -funsigned-char 

              -fwritable-strings -traditional -traditional-cpp 

              -trigraphs 

 

       编译时的警告选项 

              -fsyntax-only -pedantic -pedantic-errors -w -W 

              -Wall -Waggregate-return -Wcast-align -Wcast-qual 

              -Wchar-subscript -Wcomment -Wconversion 

              -Wenum-clash -Werror -Wformat -Wid-clash-len 

              -Wimplicit -Winline -Wmissing-prototypes 

              -Wmissing-declarations -Wnested-externs -Wno-import 

              -Wparentheses -Wpointer-arith -Wredundant-decls 

              -Wreturn-type -Wshadow -Wstrict-prototypes -Wswitch 

              -Wtemplate-debugging -Wtraditional -Wtrigraphs 

              -Wuninitialized -Wunused -Wwrite-strings 

 

       除错选项 

              -a -dletters -fpretend-float -g -glevel -gcoff 

              -gxcoff -gxcoff+ -gdwarf -gdwarf+ -gstabs -gstabs+ 

              -ggdb -p -pg -save-temps -print-file-name=library 

              -print-libgcc-file-name -print-prog-name=program 

 

       最佳化选项 

              -fcaller-saves -fcse-follow-jumps -fcse-skip-blocks 

              -fdelayed-branch -felide-constructors 

              -fexpensive-optimizations -ffast-math -ffloat-store 

              -fforce-addr -fforce-mem -finline-functions 

              -fkeep-inline-functions -fmemoize-lookups 

              -fno-default-inline -fno-defer-pop 

              -fno-function-cse -fno-inline -fno-peephole 

              -fomit-frame-pointer -frerun-cse-after-loop 

              -fschedule-insns -fschedule-insns2 

              -fstrength-reduce -fthread-jumps -funroll-all-loops 

              -funroll-loops -O -O2 

 

       预处理选项 

              -Aassertion -C -dD -dM -dN -Dmacro[=defn] -E -H 

              -idirafter dir -include file -imacros file -iprefix 

              file -iwithprefix dir -M -MD -MM -MMD -nostdinc -P 

              -Umacro -undef 

 

       汇编程序选项 

              -Wa,option 

 

       连结程序选项 

              -llibrary -nostartfiles -nostdlib -static -shared 

              -symbolic -Xlinker option -Wl,option -u symbol 

 

       目录选项 

              -Bprefix -Idir -I- -Ldir 

 

       Target Options 

              -b  machine -V version 

 

       与机器(平台)相关的选项 

              M680x0 Options 

              -m68000 -m68020 -m68020-40 -m68030 -m68040 -m68881 

              -mbitfield -mc68000 -mc68020 -mfpa -mnobitfield 

              -mrtd -mshort -msoft-float 

 

              VAX Options 

              -mg -mgnu -munix 

 

              SPARC Options 

              -mepilogue -mfpu -mhard-float -mno-fpu 

              -mno-epilogue -msoft-float -msparclite -mv8 

              -msupersparc -mcypress 

 

              Convex Options 

              -margcount -mc1 -mc2 -mnoargcount 

 

              AMD29K Options 

              -m29000 -m29050 -mbw -mdw -mkernel-registers 

              -mlarge -mnbw -mnodw -msmall -mstack-check 

              -muser-registers 

 

              M88K Options 

              -m88000 -m88100 -m88110 -mbig-pic 

              -mcheck-zero-division -mhandle-large-shift 

              -midentify-revision -mno-check-zero-division 

              -mno-ocs-debug-info -mno-ocs-frame-position 

              -mno-optimize-arg-area -mno-serialize-volatile 

              -mno-underscores -mocs-debug-info 

              -mocs-frame-position -moptimize-arg-area 

              -mserialize-volatile -mshort-data-num -msvr3 -msvr4 

              -mtrap-large-shift -muse-div-instruction 

              -mversion-03.00 -mwarn-passed-structs 

 

              RS6000 Options 

              -mfp-in-toc -mno-fop-in-toc 

 

              RT Options 

              -mcall-lib-mul -mfp-arg-in-fpregs -mfp-arg-in-gregs 

              -mfull-fp-blocks -mhc-struct-return -min-line-mul 

              -mminimum-fp-blocks -mnohc-struct-return 

 

              MIPS Options 

              -mcpu=cpu type -mips2 -mips3 -mint64 -mlong64 

              -mlonglong128 -mmips-as -mgas -mrnames -mno-rnames 

              -mgpopt -mno-gpopt -mstats -mno-stats -mmemcpy 

              -mno-memcpy -mno-mips-tfile -mmips-tfile 

              -msoft-float -mhard-float -mabicalls -mno-abicalls 

              -mhalf-pic -mno-half-pic -G num -nocpp 

 

              i386 Options 

              -m486 -mno-486 -msoft-float -mno-fp-ret-in-387 

 

              HPPA Options 

              -mpa-risc-1-0 -mpa-risc-1-1 -mkernel -mshared-libs 

              -mno-shared-libs -mlong-calls -mdisable-fpregs 

              -mdisable-indexing -mtrailing-colon 

 

              i960 Options 

              -mcpu-type -mnumerics -msoft-float 

              -mleaf-procedures -mno-leaf-procedures -mtail-call 

              -mno-tail-call -mcomplex-addr -mno-complex-addr 

              -mcode-align -mno-code-align -mic-compat 

              -mic2.0-compat -mic3.0-compat -masm-compat 

              -mintel-asm -mstrict-align -mno-strict-align 

              -mold-align -mno-old-align 

 

              DEC Alpha Options 

              -mfp-regs -mno-fp-regs -mno-soft-float -msoft-float 

 

              System V Options 

              -G -Qy -Qn -YP,paths -Ym,dir 

 

       Code Generation Options 

              -fcall-saved-reg -fcall-used-reg -ffixed-reg 

              -finhibit-size-directive -fnonnull-objects 

              -fno-common -fno-ident -fno-gnu-linker 

              -fpcc-struct-return -fpic -fPIC 

              -freg-struct-returno -fshared-data -fshort-enums 

              -fshort-double -fvolatile -fvolatile-global 

              -fverbose-asm 

 

PRAGMAS 

       Two  `#pragma'  directives  are  supported for GNU C++, to 

       permit using the same header file for two purposes:  as  a 

       definition  of  interfaces to a given object class, and as 

       the full definition of the contents of that object  class. 

 

       #pragma interface 

              (C++  only.)   Use  this  directive in header files 

              that define object classes, to save space  in  most 

              of  the  object files that use those classes.  Nor- 

              mally, local copies of certain information  (backup 

              copies of inline member functions, debugging infor- 

              mation, and the internal tables that implement vir- 

              tual  functions)  must  be kept in each object file 

              that includes class definitions.  You can use  this 

              pragma  to  avoid  such duplication.  When a header 

              file containing `#pragma interface' is included  in 

              a  compilation, this auxiliary information will not 

              be generated (unless the main input source file it- 

              self  uses `#pragma implementation').  Instead, the 

              object files will contain references to be resolved 

              at link time. 

 

       #pragma implementation 

 

       #pragma implementation "objects.h" 

              (C++  only.)  Use this pragma in a main input file, 

              when you want  full  output  from  included  header 

              files  to be generated (and made globally visible). 

              The included  header  file,  in  turn,  should  use 

              `#pragma  interface'.  Backup copies of inline mem- 

              ber functions, debugging information, and  the  in- 

              ternal  tables  used to implement virtual functions 

              are all generated in implementation files. 

 

              If you use `#pragma implementation' with  no  argu- 

              ment,  it  applies to an include file with the same 

              basename as  your  source  file;  for  example,  in 

              `allclass.cc',  `#pragma  implementation' by itself 

              is   equivalent    to    `#pragma    implementation 

              "allclass.h"'.  Use the string argument if you want 

              a single implementation file to include  code  from 

              multiple header files. 

 

              There  is no way to split up the contents of a sin- 

              gle header file into multiple implementation files. 

 

文件说明 

       file.c             C source file 

       file.h             C header (preprocessor) file 

       file.i             经预处理过的 C source file 

       file.C             C++ source file 

       file.cc            C++ source file 

       file.cxx           C++ source file 

       file.m             Objective-C source file 

       file.s             assembly language file 

       file.o             object file 

       a.out              link edited output 

       TMPDIR/cc*         temporary files 

       LIBDIR/cpp         preprocessor 

       LIBDIR/cc1         compiler for C 

       LIBDIR/cc1plus     compiler for C++ 

       LIBDIR/collect     linker front end needed on some machines 

       LIBDIR/libgcc.a    GCC subroutine library 

       /lib/crt[01n].o    start-up routine 

       LIBDIR/ccrt0       additional start-up routine for C++ 

       /lib/libc.a        standard C library, 参阅 man page intro(3) 

       /usr/include       standard directory for #include files 

       LIBDIR/include     standard gcc directory for #include files 

       LIBDIR/g++-include additional g++ directory for #include 

 

       LIBDIR is usually /usr/local/lib/machine/version. 

       TMPDIR comes from the environment variable TMPDIR (default 

       /usr/tmp if available, else /tmp).
