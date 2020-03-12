com = "Ajustes nos arquivos de configuração"

cd src/AIDA-fluxo/

git add .
git commit -m $(com)
git push

cd ../AIDA-preprocessamento-1/

git add .
git commit -m $(com)
git push

cd ../AIDA-processamento-1/

git add .
git commit -m $(com)
git push

cd ../AIDA-usercode/

git add .
git commit -m $(com)
git push

cd ../..

git add .
git commit -m $(com)
git push
