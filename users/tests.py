from django.test import TestCase


# Test Case 1: Ops User - Login
def test_ops_user_login(client):
    response = client.post('/login', json={
        'username': 'ops_user',
        'password': 'securepassword'
    })
    assert response.status_code == 200
    assert 'token' in response.json()


# Test Case 2: Ops User - Upload File
def test_ops_user_upload_file(client, ops_user_token):
    with open('test_file.pptx', 'rb') as file:
        response = client.post('/upload', 
                               headers={'Authorization': f'Bearer {ops_user_token}'}, 
                               files={'file': file})
    assert response.status_code == 200
    assert response.json()['message'] == 'File uploaded successfully'


# Test Case 3: Ops User - Invalid File Type Upload
def test_ops_user_invalid_upload(client, ops_user_token):
    with open('test_file.txt', 'rb') as file:
        response = client.post('/upload', 
                               headers={'Authorization': f'Bearer {ops_user_token}'}, 
                               files={'file': file})
    assert response.status_code == 400
    assert response.json()['message'] == 'Invalid file type. Only .pptx, .docx, .xlsx are allowed.'


# Test Case 4: Client User - Sign Up
def test_client_user_signup(client):
    response = client.post('/signup', json={
        'username': 'client_user',
        'email': 'client@example.com',
        'password': 'securepassword'
    })
    assert response.status_code == 200
    assert 'verification_url' in response.json()


# Test Case 5: Client User - Email Verification
def test_client_user_email_verification(client):
    verification_url = 'some_encrypted_url'
    response = client.get(f'/email-verify/{verification_url}')
    assert response.status_code == 200
    assert response.json()['message'] == 'Email verified successfully'


# Test Case 6: Client User - Download File
def test_client_user_download_file(client, client_user_token, file_id):
    response = client.get(f'/download-file/{file_id}', 
                          headers={'Authorization': f'Bearer {client_user_token}'})
    assert response.status_code == 200
    assert 'download-link' in response.json()


# Test Case 7: Unauthorized Access to Download Link
def test_ops_user_access_download_link(client, ops_user_token, file_id):
    response = client.get(f'/download-file/{file_id}', 
                          headers={'Authorization': f'Bearer {ops_user_token}'})
    assert response.status_code == 403
    assert response.json()['message'] == 'Access denied'


# Test Case 8: List All Uploaded Files
def test_client_user_list_files(client, client_user_token):
    response = client.get('/list-files', 
                          headers={'Authorization': f'Bearer {client_user_token}'})
    assert response.status_code == 200
    assert isinstance(response.json()['files'], list)

