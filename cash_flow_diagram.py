import pandas as pd
import matplotlib.pyplot as plt

class Drawer:
    
    def __init__(self,rd='data.xlsx', sheet_name='Cash Flow Diagram', title='Cash Flow Diagram', figsize=(5,4), legend1_loc='lower right', legend2_loc='upper right', title_fontweight='bold', colors=['#0000D9','#E63333','#FFCC33','#008000'], show_lack=False):
        self.colors = colors
        self.df = pd.read_excel(rd, sheet_name=sheet_name) # recommended xlrd version: 1.2.0
        self.title = title
        self.figsize = figsize
        self.legend1_loc = legend1_loc
        self.legend2_loc = legend2_loc
        self.title_fontweight = title_fontweight
        self.show_lack = show_lack
        
        self.fig, self.ax1 = plt.subplots(figsize=self.figsize) # ax1: the left y-axis
        self.ax2 = self.ax1.twinx() # ax2: the right y-axis
        
        self.start = self.df.at[self.df.index[0],self.df.columns[0]]
        self.end = self.df.at[self.df.index[-1],self.df.columns[0]]
        plt.xlim(self.start-1,self.end+1)
        
        plt.rcParams['axes.unicode_minus'] = False # normally display minus
        
    def get_color(self):
        self.colors.append(self.colors.pop(0))
        return self.colors[-1]
    
    def get_xposr(self,val):
        return (val-self.start+1)/(self.end-self.start+1)
    
    def get_xposl(self,val):
        return (val-self.start)/(self.end-self.start+1)
    
    def handle_lack(self):
        broken_ranges = []
        for i in self.df.index[:-1]:
            if self.df.at[i+1,self.df.columns[0]]-self.df.at[i,self.df.columns[0]] > 1:
                broken_ranges.append([self.df.at[i,self.df.columns[0]],self.df.at[i+1,self.df.columns[0]]])
                if self.show_lack:
                    begin = self.df.iloc[i].tolist()
                    end = self.df.iloc[i+1].tolist()
                    diff = [(end[j]-begin[j])/(end[0]-begin[0]) for j in range(len(begin))]
                    row = begin
                    while row[0] < end[0]-1:
                        row = [int(row[0]+1)]+[row[j]+diff[j] for j in range(1,len(row))]
                        self.df = self.df.append(pd.Series(row, index=self.df.columns), ignore_index=True)
        if self.show_lack:
            self.df.sort_values(self.df.columns[0], ignore_index=True, inplace=True)
        return broken_ranges
        
    def ax1_zero(self,broken_ranges,color='black',ls1='-',ls2='--'):
        if not self.show_lack and broken_ranges:
            self.ax1.axhline(y=0, color=color, linestyle=ls1, linewidth=1, xmax=self.get_xposr(broken_ranges[0][0]))
            for i in range(len(broken_ranges)-1):
                self.ax1.axhline(y=0, color=color, linestyle=ls2, linewidth=1, xmin=self.get_xposl(broken_ranges[i][0]), xmax=self.get_xposr(broken_ranges[i][1]))
                self.ax1.axhline(y=0, color=color, linestyle=ls1, linewidth=1, xmin=self.get_xposl(broken_ranges[i][1]), xmax=self.get_xposr(broken_ranges[i+1][0]))
            self.ax1.axhline(y=0, color=color, linestyle=ls2, linewidth=1, xmin=self.get_xposl(broken_ranges[-1][0]), xmax=self.get_xposr(broken_ranges[-1][1]))
            self.ax1.axhline(y=0, color=color, linestyle=ls1, linewidth=1, xmin=self.get_xposl(broken_ranges[-1][1]))
        else:
            self.ax1.axhline(y=0, color=color, linestyle=ls1, linewidth=1)
    
    def draw(self):
        # set labels and axises
        self.ax1.set_xlabel(self.df.columns[0],fontsize=16)
        self.ax1.set_ylabel('Income Per Year (Billion RMB)',fontsize=16)
        self.ax1.tick_params(axis='both',direction='in',labelsize=12) # set both axises' scale line direction of ax1 as 'in'
        self.ax2.set_ylabel('Total Profits (Billion RMB)',fontsize=16)
        self.ax2.tick_params(axis='both',direction='in',labelsize=12) # set both axises' scale line direction of ax2 as 'in'

        broken_ranges = self.handle_lack()
            
        # draw bars and plot
        for col in self.df.columns[1:-1]:
            self.ax1.bar(self.df[self.df.columns[0]],self.df[col],label=col,color=self.get_color())
        self.ax2.plot(self.df[self.df.columns[0]],self.df[self.df.columns[-1]],label=self.df.columns[-1],color=self.get_color())

        self.ax1_zero(broken_ranges) # draw y=0 in ax1
        self.ax2.axhline(y=0, color='black', linestyle='-', linewidth=1) # draw y=0 in ax2

        # set the legends' position and name the title
        self.ax1.legend(loc=self.legend1_loc, fontsize=12)
        self.ax2.legend(loc=self.legend2_loc, fontsize=12)
        plt.title(self.title, fontsize=24, fontweight=self.title_fontweight)
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':      
    my_drawer = Drawer()
    my_drawer.draw()
