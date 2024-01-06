import streamlit as st
from datetime import datetime
from extra_streamlit_components import CookieManager
from supabase import create_client, Client
from time import sleep
#from streamlit_javascript import st_javascript
import jwt

class Authenticate:

    def __init__(self, cookie_name: str, url: str, key_supa: str):
        """
        Create a new instance of "Authenticate".

        Parameters
        ----------
        cookie_name: str
            The name of the JWT cookie stored on the client's browser for passwordless reauthentication.
        url: str
            The url of supabase project.
        key_supa: str
            The key of supabase project.
        cookie_expiry_days: float
            The number of days before the cookie expires on the client's browser.
        """
        self.cookie_name = cookie_name
        self.key = key_supa
        self.url = url
        self.cookie_manager = CookieManager()
        self.supabase: Client = create_client(self.url, self.key) 
        
        if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None
        if 'email' not in st.session_state:
            st.session_state['email'] = None
        if 'logout' not in st.session_state:
            st.session_state['logout'] = None
        if 'provider' not in st.session_state:
            st.session_state['provider'] = None


    def _check_cookie(self):
        """
        Checks the validity of the reauthentication cookie.
        """
        # url = st_javascript("await fetch('').then(r => window.parent.location.href)")
        # try:
        #     urlli=url.split("#access_token=")
        # except:
        #     urlli=[]
        # if len(urlli)>1:
        #     #urlold=urlli[0]
        #     try:
        #         self.token=urlli[1].split("&")[0]
        #         self.refresh=urlli[1].split("refresh_token=")[1].split("&")[0]
        #         sleep(0.01)
        #         self.cookie_manager.set(self.cookie_name, self.token, key="token")
        #         sleep(0.01)
        #         self.cookie_manager.set("provider", self.refresh, key="refresh")
        #         st.session_state['provider'] = True
        #     except:
        #         st.session_state['provider'] = False
        self.token = self.cookie_manager.get(self.cookie_name)
        if self.token is not None:
            self.token = jwt.decode(self.token, options={"verify_signature": False})
            if self.token is not False:
                if not st.session_state['logout']:
                    if self.token['exp'] > datetime.now().timestamp():
                        if 'email' in self.token:
                            st.session_state['email'] = self.token['email']
                            if st.session_state['provider']:
                                st.session_state['authentication_status'] = None
                            else:
                                st.session_state['authentication_status'] = True

    
    def _check_credentials(self, email, password) -> bool:
        try:
            user_check = self.supabase.auth.sign_in_with_password({"email":email, "password": password})
            st.session_state['email'] = user_check.session.user.email
            self.exp_date = datetime.fromtimestamp(user_check.session.expires_at)
            self.token = user_check.session.access_token
            self.refresh=user_check.session.refresh_token
            sleep(0.01)
            self.cookie_manager.set(self.cookie_name, self.token,
                expires_at=self.exp_date)
            sleep(0.01)
            self.cookie_manager.set("provider", self.refresh, key="refresh2")
            st.session_state['authentication_status'] = True
        except:
            st.session_state['authentication_status'] = False


    def login(self, form_name: str, location: str='main', providers: list=[]) -> tuple:
        """
        Creates a login widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the login form.
        location: str
            The location of the login form i.e. main or sidebar.
        Returns
        -------
        bool
            The status of authentication, None: no credentials entered, 
            False: incorrect credentials, True: correct credentials.
        str
            email of the authenticated user.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")

        if location == 'main':
            c = st.columns([2,1,2])
            with c[1]:
                st.image("logo-cvc.png",width=200)
            place=st.empty()
        elif location == 'sidebar':
            place=st.sidebar.empty()
            
        self._check_cookie()
        if not st.session_state['authentication_status']:
            if not st.session_state['provider']:
                login_form=place.form(form_name)
                login_form.subheader(form_name)
                self.email = login_form.text_input('Usuario')
                st.session_state['email'] = self.email
                self.password = login_form.text_input('Contraseña', type='password')

                if login_form.form_submit_button('Ingresar', type="primary"):
                    self._check_credentials(self.email,self.password)
                
                # if len(providers)>0:
                #     with place2.container():
                #         st.markdown(f"""<p style='display: block; text-align: center;'> O continúa con: </p>""", unsafe_allow_html=True)
                #         #namesp={"github":"GitHub", "google":"Google", "facebook":"Facebook", "linkedin":"LinkedIn"}
                #         imagsp={"github":"https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg", 
                #                 "google":"https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg", 
                #                 "facebook":"https://upload.wikimedia.org/wikipedia/commons/f/fb/Facebook_icon_2013.svg", 
                #                 "linkedin":"https://upload.wikimedia.org/wikipedia/commons/8/81/LinkedIn_icon.svg"}
                #         cols=st.columns(len(providers))
                #         for i in range(len(providers)):
                #             with cols[i]:
                #                 p=providers[i]
                #                 datap = self.supabase.auth.sign_in_with_oauth({"provider": p})
                #                 p_url=datap.url
                #                 st.markdown(f"""<a style='display: block; text-align: center;' href="{p_url}" target="_self"><img src="{imagsp[p]}" height="15%" width="15%" /></a>""", unsafe_allow_html=True)

            # if st.session_state['provider']:
            #     url = st_javascript("await fetch('').then(r => window.parent.location.href)", key="segurl")
            #     try:
            #         urlli=url.split("#access_token=")
            #     except:
            #         urlli=[]
            #     if len(urlli)>1:
            #         urlold=urlli[0]
            #         with place.container():
            #             st.write("Te has logueado satisfactoriamente con el proveedor externo")
            #             st.markdown(f'<a href="{urlold}" target="_self">Continuar</a>', unsafe_allow_html=True)

        return st.session_state['authentication_status'], st.session_state['email']

    def logout(self, button_name: str, location: str='main'):
        """
        Creates a logout button.

        Parameters
        ----------
        button_name: str
            The rendered name of the logout button.
        location: str
            The location of the logout button i.e. main or sidebar.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            if st.button(button_name):
                #self.refresh = self.cookie_manager.get("provider")
                #if self.refresh is not None:
                #    st.write(self.refresh)
                #    self.supabase.auth.refresh_session(self.refresh)
                #    self.supabase.auth.sign_out()
                #    self.cookie_manager.delete("provider", key="del_prov")
                self.supabase.auth.sign_out()
                st.session_state['logout'] = True
                st.session_state['email'] = None
                st.session_state['authentication_status'] = None
                #st.session_state['provider'] = None
                self.cookie_manager.delete(self.cookie_name)
        elif location == 'sidebar':  
            if st.sidebar.button(button_name):
                self.refresh = self.cookie_manager.get("provider")
                if self.refresh is not None:
                    self.supabase.auth.refresh_session(self.refresh)
                    self.supabase.auth.sign_out()
                    self.cookie_manager.delete("provider", key="del_prov")
                st.session_state['logout'] = True
                st.session_state['email'] = None
                st.session_state['authentication_status'] = None
                st.session_state['provider'] = None
                self.cookie_manager.delete(self.cookie_name)


                
