"""Gera as figuras da Aula 02 a partir dos CSVs trimestrais do SIDRA.

Decisoes de forma, derivadas da validacao computacional da paleta (dataviz) e
das proprias unidades dos dados:

1. Serie unica por grafico, em roxo #2e2640. Medido: luminosidade 0,29 e croma
   0,048, ou seja, o roxo se comporta como tinta e nao como cor de serie. O
   coral entra so como destaque, que e a regra de proporcao do brandbook p.68.
2. A paleta do segmento Graduacao REPROVA para cinco series categoricas: os
   dois cinzas tem deltaE 7,5 entre si, abaixo do piso de 15, ou seja, nem
   quem enxerga todas as cores os distingue. Por isso painel multiplo.
3. As cinco series tem UNIDADES DIFERENTES (kg, mil duzias, mil litros).
   Sobrepor exigiria dois eixos, que e o erro numero um de grafico.
4. O grafico do descompasso NAO interpola os pontos mensais. Mostrar valores
   mensais inventados seria cometer, no grafico, o erro que a aula ensina a
   evitar. A cadencia aparece como faixa estrutural, sem valor.

Uso: python3 tools/graficos_aula02.py   (requer matplotlib)
"""
import csv, os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAIZ="/Users/joseromualdocostafilho/Projects/Inteli/Graduacao/2026.2/2026-2A-M03"
TINTA="#2e2640"; DESTAQUE="#ff4545"; SUAVE="#caced6"; FUNDO="#ffffff"

with open(os.path.join(RAIZ,"dados","abate_bovinos.csv"),encoding="utf-8") as fh:
    L=[l for l in csv.DictReader(fh) if l["valor"]]
per=[l["periodo"] for l in L][-24:]; val=[float(l["valor"]) for l in L][-24:]
xs=list(range(len(per)))

fig,(ax,cad)=plt.subplots(2,1,figsize=(12,5.0),dpi=160,
                          gridspec_kw={"height_ratios":[4,1],"hspace":0.35})
fig.patch.set_facecolor(FUNDO)

# painel de cima: so o dado que existe
ax.plot(xs,[v/1e9 for v in val],color=TINTA,linewidth=2,zorder=3)
ax.scatter(xs,[v/1e9 for v in val],s=30,color=TINTA,zorder=4,edgecolor=FUNDO,linewidth=1.4)
ax.set_ylabel("bilhoes de kg de carcaca",color=TINTA,fontsize=10)
t=[i for i,p in enumerate(per) if p.endswith("T1")]
ax.set_xticks(t); ax.set_xticklabels([per[i][:4] for i in t])
ax.set_xlim(-0.8,len(per)-0.2)
for s in ("top","right"): ax.spines[s].set_visible(False)
for s in ("left","bottom"): ax.spines[s].set_color(SUAVE); ax.spines[s].set_linewidth(0.8)
ax.tick_params(colors=TINTA,labelsize=9,length=3,width=0.8,color=SUAVE)
ax.grid(axis="y",color=SUAVE,linewidth=0.6,alpha=0.6); ax.set_axisbelow(True)
ax.set_title("Abate de bovinos, peso total das carcacas (IBGE, tabela 1092)",
             color=TINTA,fontsize=11,loc="left",pad=10)

# painel de baixo: cadencia, nao dado. Nenhum valor inventado.
cad.set_xlim(-0.8,len(per)-0.2); cad.set_ylim(-0.5,1.5)
cad.scatter(xs,[1]*len(xs),s=28,color=TINTA,zorder=3)
mens=[i+k/3 for i in range(len(per)) for k in (0,1,2)]
cad.scatter(mens,[0]*len(mens),s=16,facecolor="none",edgecolor=DESTAQUE,linewidth=1.1,zorder=3)
cad.text(-0.5,1.0,"o IBGE mede: 24 observacoes",color=TINTA,fontsize=9.5,ha="right",va="center")
cad.text(-0.5,0.0,"o TAPI pediu: 72, sendo 48 nunca medidas",color=DESTAQUE,fontsize=9.5,ha="right",va="center")
cad.axis("off")

fig.subplots_adjust(left=0.245,right=0.985,top=0.90,bottom=0.06)
d=os.path.join(RAIZ,"assets","img","aula02-descompasso-granularidade.png")
fig.savefig(d,facecolor=FUNDO); print("gerado:",d)


# ---- painel multiplo das cinco series ----
def ler(n):
    with open(os.path.join(RAIZ,"dados",n),encoding="utf-8") as fh:
        L=[l for l in csv.DictReader(fh) if l["valor"]]
    return [l["periodo"] for l in L],[float(l["valor"]) for l in L]
S=[("abate_frangos.csv","Frangos",1e9,"bi de kg"),
   ("abate_bovinos.csv","Bovinos",1e9,"bi de kg"),
   ("abate_suinos.csv","Suinos",1e9,"bi de kg"),
   ("producao_ovos.csv","Ovos",1e6,"bi de duzias"),
   ("producao_leite.csv","Leite",1e6,"bi de litros")]
fig,axes=plt.subplots(1,5,figsize=(13.5,3.4),dpi=160); fig.patch.set_facecolor(FUNDO)
for ax,(arq,tit,div,uni) in zip(axes,S):
    per,val=ler(arq); per,val=per[-60:],[v/div for v in val[-60:]]
    xs=list(range(len(per)))
    ax.plot(xs,val,color=TINTA,linewidth=1.6)
    ax.set_title(tit,color=TINTA,fontsize=12,pad=6)
    ax.set_ylabel(uni,color=TINTA,fontsize=8.5,labelpad=2)   # unidade no eixo CERTO
    t=[i for i,p in enumerate(per) if p.endswith("T1") and int(p[:4])%5==0]
    ax.set_xticks(t); ax.set_xticklabels([per[i][:4] for i in t],fontsize=8.5)
    ax.set_ylim(bottom=0)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    for s in ("left","bottom"): ax.spines[s].set_color(SUAVE); ax.spines[s].set_linewidth(0.8)
    ax.tick_params(colors=TINTA,labelsize=8.5,length=3,width=0.8,color=SUAVE)
    ax.grid(axis="y",color=SUAVE,linewidth=0.6,alpha=0.55); ax.set_axisbelow(True)
fig.suptitle("As cinco series do case, cada uma na sua unidade (IBGE, base trimestral)",
             color=TINTA,fontsize=11,x=0.008,ha="left",y=0.99)
fig.tight_layout(rect=[0,0,1,0.93])
d=os.path.join(RAIZ,"assets","img","aula02-cinco-series.png")
fig.savefig(d,facecolor=FUNDO); print("gerado:",d)
