import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('C:/Users/42077/OneDrive/Documents/PythonScripts/Scientific_plot/scientific.mplstyle')

data = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv')



if __name__ == '__main__':
    time_start = input('Enter start date (in format year-month-day): ')  # gets users time start input 
    time_stop = input('Enter stop date (in format year-month-day): ')  # gets users time stop input
    countries = np.array(input('Enter desired countries (separate them with "," without space): ').split(','))  #creates a list of countries (type str) from the input
    print(data.keys())  # prints the list of plottable variables for the user to choose
    to_plot_y1 = np.array(input('From the list above select the data to be plotted on y1 axis (separate each with a single space): ').split(' '))  # vars to plot on left y axis
    to_plot_y2 = np.array(input('From the list above select the data to be plotted on y2 axis (separate each with a single space): ').split(' '))  # vars to plot on right y axis
    
    fig_save = input('Would you like to save the final figure (y/n)? ')
    
    if str(fig_save) == 'y':
        fig_name = input('Enter the name of the figure (final plot will be saved under this name): ')
        fig_type = input('Choose desired format (pdf, png, jpg): ')
        fig_dpi = input('Choose image resolution - dpi (300 - 600 recommended): ')
        
    fig = plt.figure()
    plot1 = fig.add_subplot(111)
    plot2 = plot1.twinx()
    plts = []  # plotted lines will be added to this list (just for a merged legend)
    
    
    for a in countries:
        data2 = data.loc[lambda x: x['location'] == a, :]  # takes only the data for a specified country (country a)
        
        if len(np.where(data2.date == time_start)[0]) == 0:     # if the time start value entered by the user is too small, we take the first value in list
            start_index = int(np.where(data2.date == data2.date.iloc[0])[0])
        else:
            start_index = int(np.where(data2.date == time_start)[0])
            
        if len(np.where(data2.date == time_stop)[0]) == 0:    # similar to time start (stop date not in list --> we take the last one in the list)
            stop_index = int(np.where(data2.date == data2.date.iloc[-1])[0])
        else:
            stop_index = int(np.where(data2.date == time_stop)[0])
            
        data3 = data2.iloc[start_index : stop_index]  # selects data from the country list that lie in the entered time interval 
        for var in to_plot_y1:
            name = str(var).replace("_", " ").capitalize()  # for nice plot labels
            ax1 = plot1.plot(pd.to_datetime(data3.date), data3[var], label = name + ' - ' + str(a)) 
            plts += ax1  # adds plots to plts list ---> will be used for one merged legend
            
            
        for var in to_plot_y2:
            name = str(var).replace("_", " ").capitalize()
            ax2 = plot2.plot(pd.to_datetime(data3.date), data3[var], label = name + ' - ' + str(a), ls = '--')
            plts += ax2
            
    
    y1 = ''
    y2 = ''
    
    # take vars from users input and transform them to strings separated by commas with the first letter cappital ---> axes labels
    
    for var1 in to_plot_y1:
        y1 = y1 + str(var1).replace("_", " ").capitalize() + ", "
    
    for var2 in to_plot_y2:
        y2 = y2 + str(var2).replace("_", " ").capitalize() + ", "
        
    y1 = y1[:-2]  # deletes last two strings (a comma and a space)
    y2 = y2[:-2]
    plot1.set_ylabel(y1)
    plot1.set_xlabel('Date')
    plot2.set_ylabel(y2)
    #plot1.legend(fontsize = 7)
    #plot2.legend(fontsize = 7)
    labs = [l.get_label() for l in plts]
    plot1.legend(plts, labs, loc = 0, fontsize = 8)
    
    if str(fig_save) == 'y':
        plt.savefig(str(fig_name) + "." + str(fig_type), dpi = int(fig_dpi))
        
    #plt.show()
    
    
    
    
        
    
    