"""
Checks a file of closures for a dataset and minimum support against
a precomputed reference file. Assumes nothing about the order.
"""

import tkinter
from tkinter import filedialog
from tkinter import font

from collections import defaultdict # Counter

from dataset import Dataset
from hyperparam import HyperParam

class OurDDict(defaultdict):
    "Just to tune how it is written out"

    def __init__(self):
        super().__init__(set)
        self.mxsuppref = 0
        self.mnsuppref = float("inf")

    def __str__(self):
        r = str()
        for s in reversed(range(self.mnsuppref, self.mxsuppref + 1)):
            r += '\n' + str(s) + ' '
            r += '\n  '.join(('{ ' + 
                (', '.join(it for it in sorted(itst))) + ' }') 
                for itst in refdict[s])
        return r

class Checker:

    def __init__(self):

        self.reffile = None
        self.clofile = None
        self.filext = ".txt" # assumed default for all files

        self.root = tkinter.Tk()

        button_width = 35
        button_height = 5
        text_width = 92
        text_height = 17

        main_frame = tkinter.Frame(self.root)
        main_frame.pack(side = tkinter.LEFT)

        self.reffilepick = tkinter.Button(main_frame)
        self.reffilepick.configure(text = "Choose a reference file",
                               width = button_width,
                               height = button_height,
                               command = self.choose_reffile)
        self.reffilepick.pack()

        self.clofilepick = tkinter.Button(main_frame)
        self.clofilepick.configure(text = "Choose a file to check",
                               width = button_width,
                               height = button_height,
                               command = self.choose_clofile)
        self.clofilepick.pack()

        self.runbutton = tkinter.Button(main_frame)
        self.runbutton.configure(text = "Check",
                                  state = tkinter.DISABLED,
                                  width = button_width,
                                  height = button_height,
                                  command = self.run)
        self.runbutton.pack()

        console_frame = tkinter.LabelFrame(self.root, text="Console")
        console_frame.pack(side = tkinter.RIGHT)
        self.console = tkinter.Text(console_frame)
        self.console.configure(width = text_width, 
                              height = text_height)
        self.console.pack(side = tkinter.LEFT)
        self.scrollY = tkinter.Scrollbar(console_frame,
                                    orient = tkinter.VERTICAL,
                                    command = self.console.yview)
        self.scrollY.pack(side = tkinter.LEFT, fill = tkinter.Y)
        self.console.configure(yscrollcommand = self.scrollY.set)

        self.root.mainloop()

    def choose_reffile(self):
        fnm = filedialog.askopenfilename(
            defaultextension = self.filext, 
            filetypes = [("text files","*.txt"), 
                         ("all files","*.*")],
            title = "Choose a reference file")
        if fnm:
            "dialog possibly canceled, but maybe actual file chosen"
            self.reffile = open(fnm)
            self.report("Opened reference file:", fnm)
            if self.clofile:
                self.runbutton.configure(state = tkinter.NORMAL)

    def choose_clofile(self):
        fnm = filedialog.askopenfilename(
            defaultextension = self.filext, 
            filetypes = [("text files","*.txt"), 
                         ("all files","*.*")],
            title = "Choose a file to be checked")
        if fnm:
            "dialog possibly canceled, but maybe actual file chosen"
            self.clofile = open(fnm)
            self.report("Opened file to check:", fnm)
            if self.reffile: 
                self.runbutton.configure(state = tkinter.NORMAL)
            self.outfnm = fnm.removesuffix(self.filext) + \
                          "_diff" + self.filext

    def report(self, *messages):
        for message in messages:
            self.console.insert(tkinter.END, message + '\n')
            self.console.see("end-2c")
            self.console.update()


    def run(self):

        refdict = OurDDict()
        for line in self.reffile:
            if line.strip():
                if '/' not in line:
                    print("!!!! ref", line)
                    exit(1)
                itst, spp = line.split('/')
                spp = int(spp)
                refdict.mxsuppref = max(refdict.mxsuppref, spp)
                refdict.mnsuppref = min(refdict.mnsuppref, spp)
                refdict[spp].add((frozenset(itst.split(',')), spp))
        self.reffile.close()
    
        clodict = OurDDict()
        for line in self.clofile:
            if line.strip():
                itst, spp = line.split('/')
                spp = int(spp)
                clodict.mxsuppref = max(clodict.mxsuppref, spp)
                clodict.mnsuppref = min(clodict.mnsuppref, spp)
                clodict[spp].add((frozenset(itst.split(',')), spp))
        self.clofile.close()

        if clodict.mnsuppref == refdict.mnsuppref and \
           clodict.mxsuppref == refdict.mxsuppref:
            suppmatch = "Support limits match."
            mnsuppref = clodict.mnsuppref
            mxsuppref = refdict.mxsuppref
            limmatch = '.'
        else:
            suppmatch = "Support limits don't match."
            mnsuppref = max(clodict.mnsuppref, refdict.mnsuppref)
            mxsuppref = min(clodict.mxsuppref, refdict.mxsuppref)
            limmatch = ' in the common supports.'

        difCR = set()
        difRC = set()
        for s in reversed(range(mnsuppref, mxsuppref + 1)):
            difCR.update(clodict[s] - refdict[s])
            difRC.update(refdict[s] - clodict[s])
        outfile = None
        if difCR or difRC:
            outfile = open(self.outfnm, 'w')
            self.report(suppmatch, 
                     "Closures don't coincide" + limmatch,
                    f"There are {len(difRC) + len(difCR)} differences"
                    + limmatch,
                    f"Differences written into file {self.outfnm}.")
        else:
            self.report(suppmatch, 
             f"Testing on common supports, {mnsuppref} to {mxsuppref}.",
              "Closures coincide" + limmatch)
        cnt = 0
        if difCR:
            print("In checked file, not in reference:", file = outfile)
            for e in sorted(difCR, key = lambda it: it[1]):
                cnt += 1
                print(f"{cnt}: {{ {', '.join(sorted(e[0]))} }} /{e[1]}",
                      file = outfile)
        if difRC:
            print("In reference, not in checked file:", file = outfile)
            for e in sorted(difRC, key = lambda it: it[1]):
                cnt += 1
                print(f"{cnt}: {{ {', '.join(sorted(e[0]))} }} /{e[1]}",
                      file = outfile)
        if outfile:
            outfile.close()
        self.runbutton.configure(state = tkinter.DISABLED)
        self.reffile = None
        self.clofile = None
        self.report("If you want to run this program again, " +
                    "please load again both files.")

        



if __name__ == "__main__":

    gui = Checker()

    # ~ checkfnm = "ref_e13_0_incomplete.txt"
    # ~ checkfnm = "ref_e13_0_.txt"
