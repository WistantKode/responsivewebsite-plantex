import subprocess
import sys
import os

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"\n[Erreur] Commande échouée : {cmd}\n{e.stderr.strip()}\n")
        return None

def get_repo_url():
    url = run_cmd("git config --get remote.origin.url")
    if not url:
        print("[Info] Aucun remote 'origin' trouvé.")
        url = input("Entrez l'URL du dépôt Git à utiliser : ").strip()
        if url:
            run_cmd(f"git remote add origin {url}")
            print(f"[OK] Remote 'origin' ajouté : {url}")
        else:
            print("[Erreur] URL non fournie. Abandon.")
            sys.exit(1)
    return url

def check_git_repo():
    if not os.path.isdir(".git"):
        print("[Erreur] Ce dossier n'est pas un dépôt Git.")
        init = input("Voulez-vous initialiser un dépôt Git ici ? (o/n) : ").lower()
        if init == "o":
            run_cmd("git init")
            print("[OK] Dépôt Git initialisé.")
        else:
            print("Abandon.")
            sys.exit(1)

def main():
    print("=== Script de push automatique sur GitHub ===\n")

    check_git_repo()
    repo_url = get_repo_url()

    print(f"[Info] Dépôt distant : {repo_url}")

    status = run_cmd("git status --porcelain")
    if not status:
        print("[Info] Aucun changement à commit. Rien à push.")
        sys.exit(0)

    print("[Info] Fichiers modifiés :")
    print(status)

    commit_msg = input("\nEntrez le message de commit : ").strip()
    if not commit_msg:
        print("[Erreur] Message de commit vide. Abandon.")
        sys.exit(1)

    run_cmd("git add .")
    print("[OK] Fichiers ajoutés à l'index.")

    commit_result = run_cmd(f'git commit -m "{commit_msg}"')
    if not commit_result:
        print("[Erreur] Commit échoué. Vérifiez les fichiers à commit.")
        sys.exit(1)
    print("[OK] Commit effectué.")

    branch = run_cmd("git rev-parse --abbrev-ref HEAD")
    if not branch:
        branch = "main"
        print(f"[Info] Utilisation de la branche par défaut : {branch}")

    print(f"[Info] Push sur la branche : {branch}")
    push_result = run_cmd(f"git push origin {branch}")
    if push_result is None:
        print("[Erreur] Push échoué. Essayez de vérifier vos accès ou l'URL du remote.")
        sys.exit(1)
    print("[OK] Push réussi !")

    print("\n=== Opération terminée avec succès ===")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[Interruption] Script arrêté par l'utilisateur.")
    except Exception as e:
        print(f"\n[Erreur inattendue] {e}")