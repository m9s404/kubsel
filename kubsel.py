import inquirer
from kubernetes import client, config
from kubeconfig import KubeConfig
from colorama import Fore, Back, Style


config.load_kube_config()
conf = KubeConfig()
client_v1 = client.CoreV1Api()


def set_cluster(cluster):
    conf.use_context(cluster)


def set_namespace(namespace):
    conf.set_context(conf.current_context(), namespace=namespace, cluster=conf.current_context())


def get_clusters() -> list:
    info_kconfig = KubeConfig().view()
    contexts = [cluster['name'] for cluster in info_kconfig['clusters']]
    return contexts


def get_namespaces() -> list:
    namespaces_list = [ns.metadata.name for ns in client_v1.list_namespace().items]
    return namespaces_list


def gen_menu(opt_list, option_name, option_message) -> str:
    template_menu = [inquirer.List(option_name,
                                   message=option_message,
                                   choices=opt_list)]
    main_opt = inquirer.prompt(template_menu)
    return main_opt[option_name]


def namespace_menu():
    print(f"You're in the cluster {Fore.LIGHTBLUE_EX}>> {conf.current_context()} << {Fore.RESET}")
    namespace_list = get_namespaces()
    namespace_selected = gen_menu(
        opt_list=namespace_list,
        option_name='namespace',
        option_message='Set your Namespace: ')
    set_namespace(namespace_selected)
    print(f'{Fore.LIGHTBLUE_EX}Your current default namespace is {Style.BRIGHT}{Back.GREEN + namespace_selected}')


def cluster_menu():
    cluster_list = get_clusters()
    cluster_list.append('Back to Main Menu')

    cluster_selected = gen_menu(
        opt_list=cluster_list,
        option_name='cluster',
        option_message='Choose your cluster: ')
    menu() if cluster_selected == 'Back to Main Menu' else set_cluster(cluster_selected)
    print(f'{Fore.LIGHTBLUE_EX}Cluster {Style.BRIGHT}{Back.GREEN + conf.current_context()}{Back.RESET}{Style.NORMAL} has been selected')


def menu():
    main_menu_list = ['Select Cluster', 'Set Namespace', 'exit']
    main_opt = gen_menu(
        opt_list=main_menu_list,
        option_name='mainopt',
        option_message='Choose your option: ')

    if main_opt == main_menu_list[1]:
        namespace_menu()
    elif main_opt == main_menu_list[0]:
        cluster_menu()
    else:
        exit(1)


def program_name():
    kubesel = '''
    ██╗  ██╗██╗   ██╗██████╗ ███████╗███████╗███████╗██╗     
    ██║ ██╔╝██║   ██║██╔══██╗██╔════╝██╔════╝██╔════╝██║     
    █████╔╝ ██║   ██║██████╔╝█████╗  ███████╗█████╗  ██║     
    ██╔═██╗ ██║   ██║██╔══██╗██╔══╝  ╚════██║██╔══╝  ██║     
    ██║  ██╗╚██████╔╝██████╔╝███████╗███████║███████╗███████╗
    ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝╚══════╝ 
    
    '''
    return kubesel


if __name__ == '__main__':
    print(program_name())
    menu()
