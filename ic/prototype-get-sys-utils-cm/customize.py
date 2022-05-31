from cmind import utils
import os

def preprocess(i):

    os_info = i['os_info']

    env = i['env']
    new_env = i['new_env']

    # Test (not needed - will be removed)
    for env_to_check in [env, new_env]:
        if env_to_check.get('CM_SKIP_SYS_UTILS','').lower() in [True, 'yes', 'on']:
            return {'return':0, 'skip':True}

    # If windows, download here otherwise use run.sh
    if os_info['platform'] == 'windows':

        automation = i['automation']

        cm = automation.cmind

        path = os.getcwd()

        clean_dirs = env.get('CM_CLEAN_DIRS','').strip()
        if clean_dirs!='':
            import shutil
            for cd in clean_dirs.split(','):
                if cd != '':
                    if os.path.isdir(cd):
                        print ('Clearning directory {}'.format(cd))
                        shutil.rmtree(cd)

        url = env['CM_PACKAGE_WIN_URL']

        print ('Downloading from {}'.format(url))

        r = cm.access({'action':'download_file', 
                       'automation':'utils,dc2743f8450541e3', 
                       'url':url})
        if r['return']>0: return r

        filename = r['filename']

        print ('Unzipping file {}'.format(filename))

        r = cm.access({'action':'unzip_file', 
                       'automation':'utils,dc2743f8450541e3', 
                       'filename':filename})
        if r['return']>0: return r

        if os.path.isfile(filename):
            print ('Removing file {}'.format(filename))
            os.remove(filename)

        # Add to path
        new_env['+PATH']=[os.path.join(path, 'bin')]

    else:
        print ('')
        print ('*******************************************************************')
        print ('This IC will attempt to install minimal system dependencies for CM.')
        print ('Note that you may be asked for your SUDO password ...')
        print ('*******************************************************************')

    return {'return':0}
