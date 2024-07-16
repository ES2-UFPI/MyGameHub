import streamlit as st

def profile_page(username):
    st.title('Editar Perfil')
    
    user = session.query(users).filter(users.c.username == username).first()
    profile = session.query(profiles).filter(profiles.c.user_id == user.id).first()
    
    if profile:
        full_name = st.text_input('Nome Completo', value=profile.full_name)
        bio = st.text_area('Bio', value=profile.bio)
        profile_picture = st.file_uploader('Foto de Perfil', type=['png', 'jpg', 'jpeg'])
        
        if profile_picture:
            image_path = os.path.join('profile_pictures', profile_picture.name)
            with open(image_path, 'wb') as f:
                f.write(profile_picture.getbuffer())
        else:
            image_path = profile.profile_picture
        
        if st.button('Salvar'):
            session.execute(profiles.update().where(profiles.c.user_id == user.id).values(
                full_name=full_name,
                bio=bio,
                profile_picture=image_path
            ))
            session.commit()
            st.success('Perfil atualizado com sucesso')
    else:
        full_name = st.text_input('Nome Completo')
        bio = st.text_area('Bio')
        profile_picture = st.file_uploader('Foto de Perfil', type=['png', 'jpg', 'jpeg'])
        
        if profile_picture:
            image_path = os.path.join('profile_pictures', profile_picture.name)
            with open(image_path, 'wb') as f:
                f.write(profile_picture.getbuffer())
        else:
            image_path = None
        
        if st.button('Salvar'):
            new_profile = profiles.insert().values(
                user_id=user.id,
                full_name=full_name,
                bio=bio,
                profile_picture=image_path
            )
            session.execute(new_profile)
            session.commit()
            st.success('Perfil criado com sucesso')
    
    # Exibir a imagem de perfil
    if image_path:
        image = load_image(image_path)
        st.image(image, caption='Foto de Perfil', use_column_width=True)

def main():
    st.sidebar.title('Navegação')
    app_mode = st.sidebar.selectbox('Escolha a Página', ['Login', 'Perfil'])
    
    if app_mode == 'Login':
        st.title('Sistema de Login e Registro')
        
        menu = ["Login", "Registrar"]
        choice = st.sidebar.selectbox("Menu", menu)
        
        if choice == "Login":
            username = st.text_input('Nome de usuário', key='login_username')
            password = st.text_input('Senha', type='password', key='login_password')
            if st.button('Login'):
                user = session.query(users).filter(users.c.username == username).first()
                if user and check_password(password, user.password):
                    st.success(f'Bem-vindo {user.username}!')
                    profile_page(username)
                else:
                    st.error('Nome de usuário ou senha incorretos')
        
        elif choice == "Registrar":
            new_username = st.text_input('Nome de usuário', key='reg_username')
            new_password = st.text_input('Senha', type='password', key='reg_password')
            confirm_password = st.text_input('Confirme a senha', type='password', key='reg_confirm')
            if st.button('Registrar'):
                if new_password == confirm_password:
                    user_exist = session.query(session.query(users).filter(users.c.username == new_username).exists()).scalar()
                    if not user_exist:
                        hashed_password = hash_password(new_password).decode('utf-8')
                        new_user = users.insert().values(username=new_username, password=hashed_password)
                        session.execute(new_user)
                        session.commit()
                        st.success('Usuário criado com sucesso. Por favor, faça login.')
                    else:
                        st.error('Este nome de usuário já está em uso')
                else:
                    st.error('As senhas não correspondem')
    
    elif app_mode == 'Perfil':
        username = st.text_input('Nome de usuário', key='profile_username')
        if st.button('Editar Perfil'):
            profile_page(username)

if __name__ == "__main__":
    main()
