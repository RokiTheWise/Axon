import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Optional

class AxonBridge:
    """
    Bridge to Google Services for Axon.
    Handles authentication and initialization of the Google Drive API service.
    """
    
    # Secure scope: Restricted to files created or opened by Axon
    SCOPES: List[str] = ['https://www.googleapis.com/auth/drive.file']
    
    def __init__(self, credentials_path: str = 'credentials.json', token_path: str = 'token.json'):
        """
        Initializes the AxonBridge and builds the Google Drive service.
        
        Args:
            credentials_path: Path to the credentials.json file from Google Cloud.
            token_path: Path to save/load the user's session token.
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.creds: Optional[Credentials] = self._authenticate()
        self.drive_service = build('drive', 'v3', credentials=self.creds)

    def _authenticate(self) -> Credentials:
        """
        Handles the OAuth2 flow: loads saved tokens, refreshes them if expired, 
        or initiates a new login flow if necessary.
        """
        creds = None
        
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
            
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Critical Error: '{self.credentials_path}' is missing. "
                        "Download it from Google Cloud Console and place it in the project root."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
                
            # Save the credentials for the next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        
        return creds

    def check_connection(self) -> bool:
        """
        Quick connectivity check to verify the Drive API service is responsive.
        """
        try:
            # Simple call to list files (will be empty if drive.file scope and no files created yet)
            self.drive_service.files().list(pageSize=1).execute()
            return True
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False
