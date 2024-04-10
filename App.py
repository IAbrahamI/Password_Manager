import os
import sv_ttk
import pyperclip
import customtkinter

from PIL import Image
from tkinter import ttk

from Scripts.PasswordManager import PasswordManager
from Scripts.PasswordGenerator import PasswordGenerator
from Scripts.LanguageManager import LanguageManager
from Scripts.KeyManager import KeyManager

from dotenv import load_dotenv
load_dotenv()

class Authenticator(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # Initializes Managers
        self.keyManager = KeyManager()
        self.languageManager = LanguageManager()
        # Initializes bools
        self.login_has_PopUp = False
        self.signin_has_PopUp = False
        self.qrcode_path_Image = "_internal/otp_auth.png"
        # Initializes the GUI
        self.title(self.languageManager.get_text("app_title"))
        self.resizable(False,False)
        # Shows Registration frame and then applies frames based on inputs of user
        self.show_registration_frame()

    # Show Registration Frame
    def show_registration_frame(self):
        self.title(self.languageManager.get_text("app_title"))
        self.geometry("500x300")
        self.registration_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.registration_frame.pack(expand=True, anchor="center")
        self.registration_span_frame = customtkinter.CTkFrame(self.registration_frame)
        self.registration_span_frame.pack(fill="both", expand=True, pady=30)
        self.registration_label = customtkinter.CTkLabel(self.registration_span_frame, text= self.languageManager.get_text("reg_title"), font=("Arial", 24))
        self.registration_label.grid(row=0, column=0, columnspan=2, pady=20)
        self.registration_signin_button = customtkinter.CTkButton(self.registration_span_frame, text=self.languageManager.get_text("reg_signin"), width=160, height=40, corner_radius=10, font=("Arial", 20), command=self.show_signin_frame)
        self.registration_signin_button.grid(row=1, column=0, padx=20, pady=20)
        self.registration_login_button = customtkinter.CTkButton(self.registration_span_frame, text=self.languageManager.get_text("reg_login"), width=160, height=40, corner_radius=10, font=("Arial", 20), command=self.show_login_frame)
        self.registration_login_button.grid(row=1, column=1, padx=20, pady=20)
        self.registration_language = customtkinter.CTkOptionMenu(self.registration_frame, values=[self.languageManager.get_text("nav_sys_lan_eng"), self.languageManager.get_text("nav_sys_lan_spa"), self.languageManager.get_text("nav_sys_lan_ger")], anchor='center', command=self.change_language_event)
        self.registration_language.pack(side='bottom', pady=20, expand=False, anchor='s')

    # Show Sign In Frame
    def show_signin_frame(self):
        self.destroy_previews_frame(self.registration_frame)
        self.title(self.languageManager.get_text("app_title"))
        self.geometry("800x600")
        # Show Sign In Frame
        self.signin_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.signin_frame.pack(fill="both", expand=True, anchor="center")
        self.signin_span_frame = customtkinter.CTkFrame(self.signin_frame)
        self.signin_span_frame.pack(pady=20, padx=40, fill="both", expand=True, anchor="center")
        self.signin_title_Label = customtkinter.CTkLabel(self.signin_span_frame, text=self.languageManager.get_text("signin_title"), font=("Arial", 24))
        self.signin_title_Label.pack(pady=40)
        self.signin_text_Label = customtkinter.CTkLabel(self.signin_span_frame, text=self.languageManager.get_text("signin_text_label"), font=("Arial", 20))
        self.signin_text_Label.pack(pady=30)
        self.signin_username_Entry = customtkinter.CTkEntry(self.signin_span_frame, placeholder_text=self.languageManager.get_text("signin_entry_placeholder"), width=200, height=35)
        self.signin_username_Entry.pack(pady=20)

        self.signin_buttons_frame = customtkinter.CTkFrame(self.signin_span_frame, fg_color='transparent')
        self.signin_buttons_frame.pack(pady=40, padx=40, anchor="s")
        self.signin_back_button = customtkinter.CTkButton(self.signin_buttons_frame, text=self.languageManager.get_text("signin_back"), height=35, font=("Arial", 16), command=lambda: self.switch_to_specific_frame(self.signin_frame, self.show_registration_frame))
        self.signin_back_button.pack(side='left', padx=20)
        self.signin_generate_button = customtkinter.CTkButton(self.signin_buttons_frame, text=self.languageManager.get_text("signin_generate"), height=35, font=("Arial", 16), command=self.generate_qrcode_and_show_frame)
        self.signin_generate_button.pack(side='left', padx=20)
        

    # Show QR Code Frame
    def show_qrcode_frame(self):
        self.destroy_previews_frame(self.signin_frame)
        self.title(self.languageManager.get_text("app_title"))
        self.qrcode_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.qrcode_frame.pack(fill="both", expand=True, anchor="center")
        self.qrcode_span_frame = customtkinter.CTkFrame(self.qrcode_frame)
        self.qrcode_span_frame.pack(pady=20, padx=20, fill="both", expand=True, anchor="center")
        self.qrcode_title_Label = customtkinter.CTkLabel(self.qrcode_span_frame, text=self.languageManager.get_text("qrcode_title"), font=("Arial", 26))
        self.qrcode_title_Label.pack(pady=20)
        self.image = Image.open(self.qrcode_path_Image)
        self.qrcode_Image = customtkinter.CTkImage(light_image=self.image, dark_image=self.image, size=(400,400))
        self.qrcode_Image_Label = customtkinter.CTkLabel(self.qrcode_span_frame, image=self.qrcode_Image, text="")
        self.qrcode_Image_Label.pack()
        self.qrcode_done_button = customtkinter.CTkButton(self.qrcode_span_frame, text=self.languageManager.get_text("qrcode_back"), height=35, font=("Arial", 16), command=self.finalize_qrcode_frame_and_properties)
        self.qrcode_done_button.pack(pady=30)

    # Show Log In Frame
    def show_login_frame(self):
        self.destroy_previews_frame(self.registration_frame)
        self.title(self.languageManager.get_text("app_title"))
        self.geometry("800x600")
        # Show Log In Frame
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.login_frame.pack(fill="both", expand=True, anchor="center")
        self.login_span_frame = customtkinter.CTkFrame(self.login_frame)
        self.login_span_frame.pack(pady=20, padx=40, fill="both", expand=True, anchor="center")
        self.login_title_Label = customtkinter.CTkLabel(self.login_span_frame, text=self.languageManager.get_text("login_title"), font=("Arial", 24))
        self.login_title_Label.pack(pady=30)
        self.login_text_Label = customtkinter.CTkLabel(self.login_span_frame, text=self.languageManager.get_text("login_username_label"), font=("Arial", 20))
        self.login_text_Label.pack(pady=20)
        self.login_username_Entry = customtkinter.CTkEntry(self.login_span_frame, placeholder_text=self.languageManager.get_text("login_username_placeholder_entry"), width=200, height=35)
        self.login_username_Entry.pack(pady=20)
        self.login_text_Label = customtkinter.CTkLabel(self.login_span_frame, text=self.languageManager.get_text("login_token_label"), font=("Arial", 20))
        self.login_text_Label.pack(pady=20)
        self.login_auth_Entry = customtkinter.CTkEntry(self.login_span_frame, placeholder_text="078437", width=100, height=35)
        self.login_auth_Entry.pack(pady=20)

        self.login_buttons_frame = customtkinter.CTkFrame(self.login_span_frame, fg_color='transparent')
        self.login_buttons_frame.pack(pady=30, padx=40, anchor="s")
        self.login_back_button = customtkinter.CTkButton(self.login_buttons_frame, text=self.languageManager.get_text("login_back"), height=32, font=("Arial", 16), command=lambda: self.switch_to_specific_frame(self.login_frame, self.show_registration_frame))
        self.login_back_button.pack(side='left', padx=20)
        self.login_button = customtkinter.CTkButton(self.login_buttons_frame, text=self.languageManager.get_text("login_generate"), height=35, font=("Arial", 16), command=self.verify_input_auth_token)
        self.login_button.pack(side='left', padx=20)
        

    # Changes language based on input selected
    def change_language_event(self, selected_language):
        self.languageManager.set_language(selected_language)
        self.registration_language.set(self.languageManager.get_language())
        self.refresh_frame()

    def refresh_frame(self):
        self.registration_frame.destroy()
        self.show_registration_frame()

    # Destroy previews Frame if exists
    def destroy_previews_frame(self, previous_frame):
        if previous_frame.winfo_exists():
            previous_frame.destroy()

    # Switches Frame to a specific Frame defined in the parameters
    def switch_to_specific_frame(self, current_frame, show_frame_function):
        self.destroy_previews_frame(current_frame)
        show_frame_function()

    # Generates QRCode and Switches Frame to QR Code Frame
    def generate_qrcode_and_show_frame(self):
        username_entry = self.signin_username_Entry.get()
        if self.signin_has_PopUp == True:
            self.login_popup_Label.destroy()
        if len(username_entry)>=3 and len(username_entry)<=48:
            if self.has_spaces(username_entry):
                text=self.languageManager.get_text("signin_popup_spaces")
                frame=self.signin_frame
                self.create_signin_popup(frame, text, 17)
                self.signin_has_PopUp = True
            else:
                self.keyManager.generate_qrCode_for_auth(username_entry)
                self.show_qrcode_frame()
        else:
            text=self.languageManager.get_text("signin_popup_lenght")
            frame=self.signin_frame
            self.create_signin_popup(frame, text, 17)
            self.signin_has_PopUp = True

    def finalize_qrcode_frame_and_properties(self):
        self.image.close()
        self.switch_to_specific_frame(self.qrcode_frame, self.show_registration_frame)
        self.keyManager.delete_qrCode()

    # Verifies if the authentication token matches and starts the Password Manager if it does
    def verify_input_auth_token(self):
        login_auth_Entry = self.login_auth_Entry.get()
        login_auth_username = self.login_username_Entry.get()
        if self.login_has_PopUp == True:
            self.login_popup_Label.destroy()
        if self.is_int(login_auth_Entry):
            if self.keyManager.verify_auth(login_auth_username, login_auth_Entry) == True:
                self.switch_to_app(login_auth_username, self.languageManager)
            else:
                text=self.languageManager.get_text("login_user_token_popup")
                frame=self.login_frame
                self.create_login_popup(frame, text, 17)
                self.login_has_PopUp = True
        else:
            text=self.languageManager.get_text("login_token_popup")
            frame = self.login_frame
            self.create_login_popup(frame, text, 20)
            self.login_has_PopUp = True

    # Check if text is int
    def is_int(self, text_entry):
        return text_entry.isdigit()
    
    # Check if string has spaces
    def has_spaces(self, input_string):
        return any(character.isspace() for character in input_string)
    
    # Pop Ups if there is something wrong
    def create_signin_popup(self, frame, text, size):
        self.login_popup_Label = customtkinter.CTkLabel(frame, text=text, font=("Arial", size))
        self.login_popup_Label.pack(pady=20)

    def create_login_popup(self, frame, text, size):
        self.login_popup_Label = customtkinter.CTkLabel(frame, text=text, font=("Arial", size))
        self.login_popup_Label.pack(pady=20)

    # Window switch from Authentication to App
    def switch_to_app(self, user, languageManager):
        self.withdraw()
        self.app = App(self, user, languageManager)
        self.app.focus()

    def on_second_window_close(self):
        self.app.destroy()
        self.switch_to_specific_frame(self.login_frame, self.show_registration_frame)
        self.deiconify()  # Show the main window when the second window is closed

class App(customtkinter.CTkToplevel):
    def __init__(self, master, user, languageManagerMain):
        super().__init__(master)
        # Initializes the Managers 
        self.passwordManager = PasswordManager(user)
        self.passwordGenerator = PasswordGenerator()
        self.languageManager = languageManagerMain
        # Initializes the GUI
        self.title(self.languageManager.get_text("app_title"))
        self.geometry("1050x700")
        self.resizable(False,True)
        sv_ttk.set_theme("Dark")
        # Set Grid 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        # Set bools
        self.remove_has_Warning = False
        self.add_has_Warning = False
        self.modify_has_Warning = False
        self.genpwd_has_PopUp = False
        self.set_main_frame()
        self.protocol("WM_DELETE_WINDOW", master.on_second_window_close)

    def set_main_frame(self):
        # Navigation Frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        # Navigation Label
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=self.languageManager.get_text("nav_title"),compound="left", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=10, pady=20)

        # Home Button
        self.navigation_home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text=self.languageManager.get_text("nav_pwd"),fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=self.home_button_event)
        self.navigation_home_button.grid(row=1, column=0, sticky="ew")

        # Add Button
        self.navigation_add_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text=self.languageManager.get_text("nav_add"),fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=self.add_button_event)
        self.navigation_add_button.grid(row=2, column=0, sticky="ew")

        # Modify Button
        self.navigation_modify_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text=self.languageManager.get_text("nav_modify"),fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=self.modify_button_event)
        self.navigation_modify_button.grid(row=3, column=0, sticky="ew")

        # Remove Button
        self.navigation_remove_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text=self.languageManager.get_text("nav_remove"),fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=self.remove_button_event)
        self.navigation_remove_button.grid(row=4, column=0, sticky="ew")

        # PasswordGenerator Button
        self.navigation_gen_password_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text=self.languageManager.get_text("nav_gen_pwd"),fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=self.genpwd_button_event)
        self.navigation_gen_password_button.grid(row=5, column=0, sticky="sew")

        # Option Menu
        self.navigation_appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=[self.languageManager.get_text("nav_sys_lan_eng"), self.languageManager.get_text("nav_sys_lan_spa"), self.languageManager.get_text("nav_sys_lan_ger")],command=self.change_language_event)
        self.navigation_appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # Option Menu
        self.navigation_appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=[self.languageManager.get_text("nav_sys_color_light"), self.languageManager.get_text("nav_sys_color_dark"), self.languageManager.get_text("nav_sys_color_system")],command=self.change_appearance_mode_event)
        self.navigation_appearance_mode_menu.grid(row=7, column=0, padx=20, pady=20, sticky="s")

        #--------------------------------------------------------------------------------------------------------------
        # Home Frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid()
        self.treeScroll = ttk.Scrollbar(self.home_frame)
        self.treeScroll.pack(side="right", fill="y")

        self.set_data_on_tree(self.home_frame)
        self.set_home_objects_frame(self.home_frame)
        #--------------------------------------------------------------------------------------------------------------
        # Add Frame
        self.add_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.add_frame.grid_columnconfigure(4, weight=1)
        self.add_span_frame = customtkinter.CTkFrame(self.add_frame)
        self.add_span_frame.pack(padx=135, fill="x", expand=True, anchor="center")
        self.add_application_name_Label = customtkinter.CTkLabel(self.add_span_frame, text=self.languageManager.get_text("add_app"), font=("Arial", 17))
        self.add_application_name_Label.grid(row=1, column=0, padx=30, pady=20, sticky="ew")
        self.add_application_name_Entry = customtkinter.CTkEntry(self.add_span_frame, placeholder_text="Outlook", height=35)
        self.add_application_name_Entry.grid(row=1, column=1, columnspan="2", padx=20, pady=20, sticky="ew")
        self.add_username_Label = customtkinter.CTkLabel(self.add_span_frame, text=self.languageManager.get_text("add_username"), font=("Arial", 17))
        self.add_username_Label.grid(row=2, column=0, padx=30, pady=20, sticky="ew")
        self.add_username_Entry = customtkinter.CTkEntry(self.add_span_frame, placeholder_text=self.languageManager.get_text("add_username_label"), height=35)
        self.add_username_Entry.grid(row=2, column=1, columnspan="2", padx=20, pady=20, sticky="ew")
        self.add_password_Label = customtkinter.CTkLabel(self.add_span_frame, text=self.languageManager.get_text("add_pwd"), font=("Arial", 17))
        self.add_password_Label.grid(row=3, column=0, padx=30, pady=20, sticky="ew")
        self.add_password_Entry = customtkinter.CTkEntry(self.add_span_frame, placeholder_text=self.languageManager.get_text("add_pwd_label"), height=35)
        self.add_password_Entry.configure(show='*')
        self.add_password_Entry.grid(row=3, column=1, columnspan="2", padx=20, pady=20, sticky="ew")
        self.add_clear_button = customtkinter.CTkButton(self.add_span_frame, text=self.languageManager.get_text("add_clear_button"), command=self.clear_all_add_inputs)
        self.add_clear_button.grid(row=4, column=1, padx=20, pady=20, sticky="ew")
        self.add_add_button = customtkinter.CTkButton(self.add_span_frame, text=self.languageManager.get_text("add_add_button"), command=self.add_entry)
        self.add_add_button.grid(row=4, column=2, padx=20, pady=20, sticky="ew")
        #--------------------------------------------------------------------------------------------------------------
        # Modify Frame
        self.modify_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.modify_frame.grid_columnconfigure(4, weight=1)
        self.modify_span_frame = customtkinter.CTkFrame(self.modify_frame)
        self.modify_span_frame.pack(padx=135, fill="x", expand=True, anchor="center")
        self.modify_id_Label = customtkinter.CTkLabel(self.modify_span_frame, text="ID", font=("Arial", 17))
        self.modify_id_Label.grid(row=0, column=0, padx=30, pady=20, sticky="ew")
        self.modify_id_Entry = customtkinter.CTkEntry(self.modify_span_frame, placeholder_text="1", height=35)
        self.modify_id_Entry.grid(row=0, column=1, columnspan="2", padx=20, pady=20, sticky="ew")
        self.modify_username_Label = customtkinter.CTkLabel(self.modify_span_frame, text=self.languageManager.get_text("modify_username"), font=("Arial", 17))
        self.modify_username_Label.grid(row=2, column=0, padx=30, pady=20, sticky="ew")
        self.modify_username_Entry = customtkinter.CTkEntry(self.modify_span_frame, placeholder_text=self.languageManager.get_text("modify_username_label"), height=35)
        self.modify_username_Entry.grid(row=2, column=1, columnspan="2", padx=20, pady=20, sticky="ew")
        self.modify_password_Label = customtkinter.CTkLabel(self.modify_span_frame, text=self.languageManager.get_text("modify_pwd"), font=("Arial", 17))
        self.modify_password_Label.grid(row=3, column=0, padx=30, pady=20, sticky="ew")
        self.modify_password_Entry = customtkinter.CTkEntry(self.modify_span_frame, placeholder_text=self.languageManager.get_text("modify_pwd_label"), height=35)
        self.modify_password_Entry.configure(show='*')
        self.modify_password_Entry.grid(row=3, column=1, columnspan="2", padx=20, pady=20, sticky="ew")
        self.modify_clear_button = customtkinter.CTkButton(self.modify_span_frame, text=self.languageManager.get_text("modify_clear_button"), command=self.clear_all_modify_inputs)
        self.modify_clear_button.grid(row=4, column=1, padx=20, pady=20, sticky="ew")
        self.modify_modify_button = customtkinter.CTkButton(self.modify_span_frame, text=self.languageManager.get_text("modify_modify_button"), command=self.modify_entry)
        self.modify_modify_button.grid(row=4, column=2, padx=20, pady=20, sticky="ew")
        #--------------------------------------------------------------------------------------------------------------
        # Remove Frame
        self.remove_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.remove_frame.grid_columnconfigure(0, weight=1)
        self.remove_span_frame = customtkinter.CTkFrame(self.remove_frame)
        self.remove_span_frame.pack(padx=120, pady=120, fill="x", expand=True, anchor="center")
        self.remove_title_Label = customtkinter.CTkLabel(self.remove_span_frame, text=self.languageManager.get_text("remove_title"), font=("Arial", 20))
        self.remove_title_Label.pack(pady=30)
        self.remove_id_Entry = customtkinter.CTkEntry(self.remove_span_frame, placeholder_text="1", height=35)
        self.remove_id_Entry.pack(pady=20)
        self.remove_delete_button = customtkinter.CTkButton(self.remove_span_frame, text=self.languageManager.get_text("remove_button"), command=self.remove_entry)
        self.remove_delete_button.pack(pady=40)
        #--------------------------------------------------------------------------------------------------------------
        # Generate Password Frame
        self.genpwd_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.genpwd_frame.grid_columnconfigure(0, weight=1)
        self.genpwd_span_frame = customtkinter.CTkFrame(self.genpwd_frame)
        self.genpwd_span_frame.pack(padx=70, pady=80, fill="both", expand=True, anchor="center")
        self.genpwd_title_Label = customtkinter.CTkLabel(self.genpwd_span_frame, text=self.languageManager.get_text("gen_title"), font=("Arial", 19))
        self.genpwd_title_Label.pack(pady=30)
        self.genpwd_characters_Label = customtkinter.CTkLabel(self.genpwd_span_frame, text=self.languageManager.get_text("gen_sub_title"), font=("Arial", 17))
        self.genpwd_characters_Label.pack()
        self.genpwd_lenght_Entry = customtkinter.CTkEntry(self.genpwd_span_frame, placeholder_text="12", height=25)
        self.genpwd_lenght_Entry.pack(pady=20)
        self.genpwd_uppercase_checkbox = customtkinter.CTkCheckBox(self.genpwd_span_frame, text=self.languageManager.get_text("gen_choise1"), corner_radius=8, font=("Arial", 17))
        self.genpwd_uppercase_checkbox.pack(padx=262, pady=10, anchor="w")
        self.genpwd_digits_checkbox = customtkinter.CTkCheckBox(self.genpwd_span_frame, text=self.languageManager.get_text("gen_choise2"), corner_radius=8, font=("Arial", 17))
        self.genpwd_digits_checkbox.pack(padx=262, pady=10, anchor="w")
        self.genpwd_punctuations_checkbox = customtkinter.CTkCheckBox(self.genpwd_span_frame, text=self.languageManager.get_text("gen_choise3"), corner_radius=8, font=("Arial", 17))
        self.genpwd_punctuations_checkbox.pack(padx=262, pady=10, anchor="w")
        self.genpwd_button = customtkinter.CTkButton(self.genpwd_span_frame, text=self.languageManager.get_text("gen_gen_button"), command=self.generate_password)
        self.genpwd_button.pack(pady=30)
        #--------------------------------------------------------------------------------------------------------------
        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.navigation_home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.navigation_add_button.configure(fg_color=("gray75", "gray25") if name == "add_frame" else "transparent")
        self.navigation_modify_button.configure(fg_color=("gray75", "gray25") if name == "modify_frame" else "transparent")
        self.navigation_remove_button.configure(fg_color=("gray75", "gray25") if name == "remove_frame" else "transparent")
        self.navigation_gen_password_button.configure(fg_color=("gray75", "gray25") if name == "generate_password_frame" else "transparent")

        # Make Button selected sticky and remove Frame if needed
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "add_frame":
            self.add_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.add_frame.grid_forget()
        if name == "modify_frame":
            self.modify_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.modify_frame.grid_forget()
        if name == "remove_frame":
            self.remove_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.remove_frame.grid_forget()
        if name == "generate_password_frame":
            self.genpwd_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.genpwd_frame.grid_forget()

    # Functions defining to show Frame based on navigation button selected
    def home_button_event(self):
        self.select_frame_by_name("home")

    def add_button_event(self):
        self.select_frame_by_name("add_frame")

    def modify_button_event(self):
        self.select_frame_by_name("modify_frame")

    def remove_button_event(self):
        self.select_frame_by_name("remove_frame")

    def genpwd_button_event(self):
        self.select_frame_by_name("generate_password_frame")

    def change_language_event(self, selected_language):
        self.languageManager.set_language(selected_language)
        self.refresh_frames()

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        if new_appearance_mode == "Dark" or new_appearance_mode == "Light":
            sv_ttk.set_theme(new_appearance_mode)
        elif new_appearance_mode == "System":
            sv_ttk.set_theme("Dark")
    #--------------------------------------------------------------------------------
    # Functions for PasswordManager       
            
    # Get Password
    def get_password_for_id(self):
        input_id = self.home_id_Entry.get()
        password = self.passwordManager.get_password_by_id(int(input_id))
        self.copy_password(password)

    # Add entry
    def add_entry(self):
        application_entry_input = self.add_application_name_Entry.get()
        username_entry_input = self.add_username_Entry.get()
        password_entry_input = self.add_password_Entry.get()
        if self.add_has_Warning == True:
            self.add_warning_Label.destroy()
        if len(application_entry_input) <= 0 or len(username_entry_input) <= 0 or len(password_entry_input) <= 0:
            frame = self.add_frame
            text=self.languageManager.get_text("add_popup")
            self.create_add_warning(frame, text, 20)
            self.add_has_Warning = True
        else:
            self.passwordManager.set_entries_to_be_stored(application_entry_input, username_entry_input, password_entry_input)
            self.add_has_Warning = False
            self.clear_text_in_entry(self.add_application_name_Entry, len(application_entry_input))
            self.clear_text_in_entry(self.add_username_Entry, len(username_entry_input))
            self.clear_text_in_entry(self.add_password_Entry, len(password_entry_input))
            self.refresh_tree_data_list(self.home_frame)
    
    def clear_all_add_inputs(self):
        application_entry_input = self.add_application_name_Entry.get()
        username_entry_input = self.add_username_Entry.get()
        password_entry_input = self.add_password_Entry.get()
        self.clear_text_in_entry(self.add_application_name_Entry, len(application_entry_input))
        self.clear_text_in_entry(self.add_username_Entry, len(username_entry_input))
        self.clear_text_in_entry(self.add_password_Entry, len(password_entry_input))

    # Modify entry by id
    def modify_entry(self):
        id_entry_input = self.modify_id_Entry.get()
        username_entry_input = self.modify_username_Entry.get()
        password_entry_input = self.modify_password_Entry.get()

        ids = self.passwordManager.get_all_ids()
        frame = self.modify_frame

        if self.modify_has_Warning == True:
            self.modify_warning_Label.destroy()
        if self.is_int(id_entry_input):
            id_as_int = int(id_entry_input)
            if id_as_int in ids:
                if len(username_entry_input) <= 0 or len(password_entry_input) <= 0:
                    text=self.languageManager.get_text("modify_all_values_popup")
                    self.create_modify_warning(frame, text, 18)
                    self.modify_has_Warning = True
                else:
                    self.passwordManager.modify_entry_in_sqlite3(id_entry_input, username_entry_input, password_entry_input)
                    self.clear_text_in_entry(self.modify_id_Entry, len(id_entry_input))
                    self.clear_text_in_entry(self.modify_username_Entry, len(username_entry_input))
                    self.clear_text_in_entry(self.modify_password_Entry, len(password_entry_input))
                    self.refresh_tree_data_list(self.home_frame)
            else:
                text=self.languageManager.get_text("modify_validID_popup")
                self.create_modify_warning(frame, text, 15)
                self.modify_has_Warning = True
        else:
            text=self.languageManager.get_text("modify_selectedID_popup")
            self.create_modify_warning(frame, text, 15)
            self.modify_has_Warning = True

    def clear_all_modify_inputs(self):
        id_entry_input = self.modify_id_Entry.get()
        username_entry_input = self.modify_username_Entry.get()
        password_entry_input = self.modify_password_Entry.get()
        self.clear_text_in_entry(self.modify_id_Entry, len(id_entry_input))
        self.clear_text_in_entry(self.modify_username_Entry, len(username_entry_input))
        self.clear_text_in_entry(self.modify_password_Entry, len(password_entry_input))

    # Remove entry by id
    def remove_entry(self):
        input_from_entry = self.remove_id_Entry.get()
        ids = self.passwordManager.get_all_ids()

        if self.remove_has_Warning == True:
            self.remove_warning_Label.destroy()
        if self.is_int(input_from_entry):
            id_as_int = int(input_from_entry)
            if id_as_int in ids:
                self.passwordManager.remove_entry_by_id(id_as_int)
                self.remove_has_Warning = False
                self.clear_text_in_entry(self.remove_id_Entry, len(input_from_entry))
                self.refresh_tree_data_list(self.home_frame)
            else:
                frame = self.remove_span_frame
                text=self.languageManager.get_text("modify_selectedID_popup")
                self.create_remove_warning(frame, text, 15)
                self.remove_has_Warning = True
        else:
            frame = self.remove_span_frame
            text=self.languageManager.get_text("remove_selectedID_popup")
            self.create_remove_warning(frame, text, 15)
            self.remove_has_Warning = True

    # Generate Password based on entries
    def generate_password(self):
        password_lenght_entry_input = self.genpwd_lenght_Entry.get()
        int_uppercase_input = self.genpwd_uppercase_checkbox.get()
        int_digits_input = self.genpwd_digits_checkbox.get()
        int_punctuations_input = self.genpwd_punctuations_checkbox.get()

        if self.genpwd_has_PopUp == True:
            self.genpwd_popup_Label.destroy()
        if self.is_int(password_lenght_entry_input) and int(password_lenght_entry_input) <= 100:
            generated_password = self.passwordGenerator.generate_password(int(password_lenght_entry_input), int_uppercase_input, int_digits_input, int_punctuations_input)
            self.copy_password(generated_password)
            frame = self.genpwd_frame
            text=self.languageManager.get_text("gen_pwd_generated_popup")
            self.create_genpwd_popup(frame, text, 17)
            self.genpwd_has_PopUp = True
        else:
            frame = self.genpwd_frame
            text=self.languageManager.get_text("gen_valid_popup")
            self.create_genpwd_popup(frame, text, 17)
            self.genpwd_has_PopUp = True

    # Check if text is int
    def is_int(self, text_entry):
        return text_entry.isdigit()
    
    # Remove text in entry
    def clear_text_in_entry(self, text_entry, end_len):
        text_entry.delete(0, end_len)
    
    # Create warnings
    def create_remove_warning(self, frame, text, size):
        self.remove_warning_Label = customtkinter.CTkLabel(frame, text=text, font=("Arial", size))
        self.remove_warning_Label.pack(pady=20)
    
    def create_add_warning(self, frame, text, size):
        self.add_warning_Label = customtkinter.CTkLabel(frame, text=text, font=("Arial", size))
        self.add_warning_Label.pack(pady=20)

    def create_modify_warning(self, frame, text, size):
        self.modify_warning_Label = customtkinter.CTkLabel(frame, text=text, font=("Arial", size))
        self.modify_warning_Label.pack(pady=20)

    def create_genpwd_popup(self, frame, text, size):
        self.genpwd_popup_Label = customtkinter.CTkLabel(frame, text=text, font=("Arial", size))
        self.genpwd_popup_Label.pack(pady=20)

    def create_home_popup(self, text):
        self.home_test_Label = customtkinter.CTkLabel(self.home_objects_frame, text=text, font=("Arial", 15))
        self.home_test_Label.grid(row=1, column=2, padx=20, pady=5)

    # Set data on tree
    def set_data_on_tree(self, frame):
        header = [[self.languageManager.get_text("pwd_id"), self.languageManager.get_text("pwd_app"), self.languageManager.get_text("pwd_username")]]
        data = header + self.passwordManager.get_all_data_from_db()
        self.tree = ttk.Treeview(frame, columns=tuple(range(len(data[0]))), show="headings", yscrollcommand=self.treeScroll.set)
        # Add data into the Tree
        for i, column_name in enumerate(data[0]):
            self.tree.heading(i, text=column_name)
            self.tree.column(i, anchor="center")
        for row_data in data[1:]:
            self.tree.insert("", "end", values=row_data)
        self.tree.pack(fill="both", expand=True)
        # Configure Scroll to match Tree
        self.treeScroll.config(command=self.tree.yview)

    def set_home_objects_frame(self, frame):
        self.home_objects_frame = customtkinter.CTkFrame(frame)
        self.home_objects_frame.pack(anchor="w")
        self.home_id_Entry = customtkinter.CTkEntry(self.home_objects_frame, placeholder_text="ID", height=35)
        self.home_id_Entry.grid(row=1, column=0, padx=20, pady=5)
        self.home_get_key_button = customtkinter.CTkButton(self.home_objects_frame, text="Get Key", command=self.get_password_for_id)
        self.home_get_key_button.grid(row=1, column=1, padx=20, pady=5)
        self.home_test_Label = customtkinter.CTkLabel(self.home_objects_frame, text="", font=("Arial", 15))
        self.home_test_Label.grid(row=1, column=2, padx=20, pady=5)

    def refresh_tree_data_list(self, frame):
        self.tree.destroy()
        self.home_objects_frame.destroy()
        self.set_data_on_tree(frame)
        self.set_home_objects_frame(frame)

    def refresh_frames(self):
        self.navigation_frame.destroy()
        self.home_frame.destroy()
        self.add_frame.destroy()
        self.modify_frame.destroy()
        self.remove_frame.destroy()
        self.title(self.languageManager.get_text("app_title"))
        self.set_main_frame()

    # Copy Password
    def copy_password(self, password):
        pyperclip.copy(password)

if __name__ == "__main__":
    main = Authenticator()
    main.mainloop()