import pandas as pd
import plotly.express as px
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox, ttk


root = Tk()
root.geometry('1000x550')
root.title('Voter Turnout By State')
root.configure(bg="white")

state_info_raw = pd.read_excel('state_info.xlsx')
state_scores_raw = pd.read_excel('scores.xlsx')
state_info_age_raw = pd.read_excel('state_info_by_age.xlsx')
state_info_sex_race_raw = pd.read_excel('state_info_by_sex_race.xlsx')

overall_scores = dict(state_scores_raw)['Score']
inperson_scores = dict(state_scores_raw)['in person']
mail_scores = dict(state_scores_raw)['mail']
abbrs = dict(state_info_raw)['ABBR']
titles = ['', 'Percent registered\n(Total)', 'Percent registered\n(Citizen)', 'Percent voted\n(Total)', 'Percent voted\n(Citizen)', 'Score', 'in person', 'mail']
    
fig_final = px.choropleth(state_info_raw, locations='ABBR', locationmode="USA-states", color='Percent voted\n(Total)', scope="usa", color_continuous_scale = 'Blues')
fig_final.write_image("map.png")

genders = [IntVar() for _ in range(2)]
[var.set(1) for var in genders]
races = [IntVar() for _ in range(8)]
[var.set(1) for var in races]
ages = [IntVar() for _ in range(5)]
[var.set(1) for var in ages]

def show_interactive():
    fig_final.show()
    
    
def edit_genders():
    child = Toplevel(root)
    child.title('Genders Selector')
    
    def change_genders():
        return 0
        
    l = Label(child, text='Select which genders you would like to include.')
    l.pack()
    
    labels = [
        'Male',
        'Female'
    ]
    
    for i in range(2):
        Checkbutton(child, text=labels[i], variable=genders[i], onvalue=1, offvalue=0, command=change_genders).pack()

    def done():
        if all(v.get() == 0 for v in genders):
            messagebox.showerror('Selection Error', 'Error: Please select at least one gender!')
            return 0
                
        child.destroy()
        update_data()
    
    done_button = Button(child, text='Done', command=done)
    done_button.pack()
    
def edit_races():
    child = Toplevel(root)
    child.title('Races Selector')

    def change_races():
        return 0
        
    l = Label(child, text='Select which races you would like to include.')
    l.pack()
    
    labels = [
        'White alone',
        'White non-Hispanic alone',
        'Black alone',
        'Asian alone',
        'Hispanic (of any race)',
        'White alone or in combination',
        'Black alone or in combination',
        'Asian alone or in combination'
    ]
    
    for i in range(8):
        Checkbutton(child, text=labels[i], variable=races[i], onvalue=1, offvalue=0, command=change_races).pack()
    
    def done():
        if all(v.get() == 0 for v in genders):
            messagebox.showerror('Selection Error', 'Error: Please select at least one race!')
            return 0
        
        child.destroy()
        update_data()
    
    done_button = Button(child, text='Done', command=done)
    done_button.pack()


def edit_ages():
    child = Toplevel(root)
    child.title('Age Ranges Selector')
    
    def change_ages():
        return 0
        
    l = Label(child, text='Select which age ranges you would like to include. Please only select continuous age ranges.')
    l.pack()
    
    labels = [
        '18 to 24', 
        '25 to 34', 
        '35 to 44', 
        '45 to 64', 
        '65+'
    ]
    
    for i in range(5):
        Checkbutton(child, text=labels[i], variable=ages[i], onvalue=1, offvalue=0, command=change_ages).pack()
    
    def done():
        if all(v.get() == 0 for v in ages):
            messagebox.showerror('Selection Error', 'Error: Please select at least one age range!')
            return 0
        
        s = ''
        for v in ages:
            s += str(v.get())
        split = s.split('0')
        while(1):
            try:
                split.remove('')
            except:
                break
        if len(split) != 1:
            messagebox.showerror('Selection Error', 'Error: Please select continous age ranges!')
            return 0
        
        child.destroy()
        update_data()
    
    done_button = Button(child, text='Done', command=done)
    done_button.pack()
    
def update_data(e=0):
    data_key = titles[data_var.get()]
    
    temp_genders = [var.get() for var in genders]
    temp_races = [var.get() for var in races]
    temp_ages = [var.get() for var in ages]
    
    g_edited = not all(v == 1 for v in temp_genders)
    r_edited = not all(v == 1 for v in temp_races)
    a_edited = not all(v == 1 for v in temp_ages)
    
    if not a_edited:
        if not (g_edited or r_edited):
            if (not (g_edited or r_edited or a_edited)):
                if data_var.get() > 4:
                    fig = px.choropleth(state_scores_raw, locations='ABBR', locationmode="USA-states", color=data_key, scope="usa", color_continuous_scale = color_selector.get())
                    fig.write_image("map.png")
                    fig_final = fig
                else:
                    fig = px.choropleth(state_info_raw, locations='ABBR', locationmode="USA-states", color=data_key, scope="usa", color_continuous_scale = color_selector.get())
                    fig.write_image("map.png")
                    fig_final = fig
        else:
            d = dict(state_info_sex_race_raw)
            tot_reg = []
            cit_reg = []
            tot_vot = []
            cit_vot = []
            for i in range(50):
                total_pop = 0
                total_cit = 0
                total_reg = 0
                total_vot = 0
                for j in range(2):
                    if genders[j].get():
                        total_pop += d['Total population'][10*i + 1 + j]
                        total_cit += d['Total citizen population'][10*i + 1 + j]
                        total_reg += d['Total registered'][10*i + 1 + j]
                        total_vot += d['Total voted'][10*i + 1 + j]
                for j in range(8):
                    if races[j].get():
                        total_pop += d['Total population'][10*i + 3 + j]
                        total_cit += d['Total citizen population'][10*i + 3 + j]
                        total_reg += d['Total registered'][10*i + 3 + j]
                        total_vot += d['Total voted'][10*i + 3 + j]
                tot_reg.append(total_reg/total_pop)
                cit_reg.append(total_reg/total_cit)
                tot_vot.append(total_vot/total_pop)
                cit_vot.append(total_vot/total_cit)     

            data_thing = {
                'ABBR': abbrs,
                'Percent registered\n(Total)': tot_reg,
                'Percent registered\n(Citizen)': cit_reg,
                'Percent voted\n(Total)': tot_vot,
                'Percent voted\n(Citizen)': cit_vot,
                'Score': overall_scores,
                'in person': inperson_scores,
                'mail': mail_scores
            }
            
            df = pd.DataFrame(data_thing)
            fig = px.choropleth(df, locations='ABBR', locationmode="USA-states", color=data_key, scope="usa", color_continuous_scale = color_selector.get())
            fig.write_image("map.png")
            fig_final = fig
    else:
        d = dict(state_info_age_raw)
        tot_reg = []
        cit_reg = []
        tot_vot = []
        cit_vot = []
        for i in range(50):
            total_pop = 0
            total_cit = 0
            total_reg = 0
            total_vot = 0
            for j in range(5):
                if ages[j].get():
                    total_pop += d['Total population'][6*i + 1 + j]
                    total_cit += d['Total citizen population'][6*i + 1 + j]
                    total_reg += d['Total registered'][6*i + 1 + j]
                    total_vot += d['Total voted'][6*i + 1 + j]
            tot_reg.append(total_reg/total_pop)
            cit_reg.append(total_reg/total_cit)
            tot_vot.append(total_vot/total_pop)
            cit_vot.append(total_vot/total_cit)     

        data_thing = {
            'ABBR': abbrs,
            'Percent registered\n(Total)': tot_reg,
            'Percent registered\n(Citizen)': cit_reg,
            'Percent voted\n(Total)': tot_vot,
            'Percent voted\n(Citizen)': cit_vot,
            'Overall Score': overall_scores
        }
        
        df = pd.DataFrame(data_thing)
        fig = px.choropleth(df, locations='ABBR', locationmode="USA-states", color=data_key, scope="usa", color_continuous_scale = color_selector.get())
        fig.write_image("map.png")
        fig_final = fig

    
    img = ImageTk.PhotoImage(Image.open("map.png"))
    label.configure(image=img)
    label.image=img    
    

interactive_button = Button(root, text='Open Interactive Map', command=show_interactive)
interactive_button.place(x=50, y=450)

gender_button = Button(root, text='Edit Included Genders', command=edit_genders)
gender_button.place(x=50, y=50)

race_button = Button(root, text='Edit Included Races', command=edit_races)
race_button.place(x=50, y=100)

ages_button = Button(root, text='Edit Included Ages', command=edit_ages)
ages_button.place(x=50, y=150)

data_var = IntVar()
data_var.set(1)

data_selector1 = Radiobutton(root, text='Percent Registered (Total)', variable=data_var, value=1, command=update_data, bg='white')
data_selector2 = Radiobutton(root, text='Percent Registered (Citizen)', variable=data_var, value=2, command=update_data, bg='white')
data_selector3 = Radiobutton(root, text='Percent Voted (Total)', variable=data_var, value=3, command=update_data, bg='white')
data_selector4 = Radiobutton(root, text='Percent Voted (Citizen)', variable=data_var, value=4, command=update_data, bg='white')
data_selector5 = Radiobutton(root, text='Overall Voter Score', variable=data_var, value=5, command=update_data, bg='white')
data_selector6 = Radiobutton(root, text='In-Person Voter Score', variable=data_var, value=6, command=update_data, bg='white')
data_selector7 = Radiobutton(root, text='Mail Voter Score', variable=data_var, value=7, command=update_data, bg='white')

data_selector1.place(x=50, y=200)
data_selector2.place(x=50, y=225)
data_selector3.place(x=50, y=250)
data_selector4.place(x=50, y=275)
data_selector5.place(x=50, y=300)
data_selector6.place(x=50, y=325)
data_selector7.place(x=50, y=350)

color_options = [
    'Blues',
    'Greens',
    'Oranges',
    'Purples',
    'Reds'
]

color_selector = ttk.Combobox(root, values=color_options)
color_selector.bind("<<ComboboxSelected>>", update_data)
color_selector.set('Blues')
color_selector.place(x=50, y=400)


img_frame = Frame(root, width=600, height=400)
img_frame.place(x=250, y=10)
img = ImageTk.PhotoImage(Image.open("map.png"))
label = Label(img_frame, image=img)
label.pack()


root.mainloop()

