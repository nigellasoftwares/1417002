import shutil
import os

def usersFolder(username):
    # Family member path
    try:
        userDocsFolder = username + 'Docs'
        user_path = f"./static/documents/"
        user_folder_path = os.path.join(user_path, userDocsFolder)
        os.makedirs(user_folder_path)
        return 'success'
    except Exception as e:
        return 'failure'



def folderCreator(userRoot, workerRegNum, status, fmPrefix, newFM_ID,  fmNum):
    if workerRegNum and status:
        workerFolder = workerRegNum
        # check Worker Folder 
        
        # Delete Existing Folder if Recreation
        folderPath = f"./static/documents/{userRoot}/{workerFolder}"
        if os.path.exists(folderPath) and os.path.isdir(folderPath):
            shutil.rmtree(folderPath)
        
        
        if os.path.exists(workerFolder) and os.path.isdir(workerFolder):
            return ("The folder exists!")
        else:
            try:
                # Worker Path
                worker_path = f"./static/documents/{userRoot}/"
                workerFolder_path = os.path.join(worker_path, workerFolder)
                os.makedirs(workerFolder_path)

                # status
                if status == 'legal':
                    status_path = f"./static/documents/{userRoot}/{workerFolder}/"
                    # if Legal
                    for x in range(1, 7):    
                        status_folder_path = os.path.join(status_path, f'doc{x}')
                        os.makedirs(status_folder_path)
                elif status == 'illegal':
                    status_path = f"./static/documents/{userRoot}/{workerFolder}/"
                    # if Legal
                    for x in range(1, 3):    
                        status_folder_path = os.path.join(status_path, f'doc{x}')
                        os.makedirs(status_folder_path)


                # Family member path
                fm_path = f"./static/documents/{userRoot}/{workerFolder}/"
                fm_folder = "familyMembers"
                fm_folder_path = os.path.join(fm_path, fm_folder)
                os.makedirs(fm_folder_path)

                # Create FM Folders
                fMember_path = f"./static/documents/{userRoot}/{workerFolder}/{fm_folder}/"
                for x in range(1, fmNum+1): 
                    # make fm registration num
                    formatted_number = f"{(int(newFM_ID) + x):06}"
                    fMemberRegistrationNumber = fmPrefix + formatted_number
                    
                    fMember_folder = fMemberRegistrationNumber   
                    fMember_folder_path = os.path.join(fMember_path, fMember_folder)
                    os.makedirs(fMember_folder_path)

                    # Docs inside Member
                    insideMember_path = f"{fMember_path}{fMember_folder}/"
                    # for doc1
                    insideMember_folder_path1 = os.path.join(insideMember_path, 'doc1')
                    os.makedirs(insideMember_folder_path1)
                    # for doc2
                    insideMember_folder_path2 = os.path.join(insideMember_path, 'doc2')
                    os.makedirs(insideMember_folder_path2)

                return "success"
            except OSError as e:
                return f"Error: {e}"
        # End Check Worker Folder
    else:
        return "Sorry! we not found, please try again."

#print(folderCreator('FW23NS000003', 'legal', 0))

