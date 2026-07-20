import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIRST = ROOT / "main.tex"
DERIV = ROOT / "大学数学I-导数与微分-中值定理讲义.tex"
OUT = ROOT / "大学数学I-完整讲义.tex"


def between(text: str, start: str, end: str | None = None) -> str:
    i = text.index(start)
    if end is None:
        return text[i:]
    j = text.index(end, i)
    return text[i:j]


def add_toc_for_starred_subsections(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        title = match.group(1)
        return rf"\subsection*{{{title}}}" + "\n" + rf"\addcontentsline{{toc}}{{subsection}}{{{title}}}"

    return re.sub(r"\\subsection\*\{([^{}]+)\}", repl, text)


first_text = FIRST.read_text(encoding="utf-8")
deriv_text = DERIV.read_text(encoding="utf-8")

first_body = between(first_text, r"\section{数列的基本概念}", r"\end{document}").strip()
deriv_body = between(
    deriv_text,
    r"\section{导数的概念}",
    r"\clearpage" + "\n" + r"\renewcommand{\refname}{References}",
).strip()

# Repair a few environment mismatches inherited from the first handout source.
first_body = first_body.replace(
    "解这个递推得 \\(H_n = 2^n - 1\\)——指数增长！64 个圆盘需要移动 \\(2^{64}-1\\) 次，即使每秒移动一次，也需要约 5849 亿年。\n\\end{custom}",
    "解这个递推得 \\(H_n = 2^n - 1\\)——指数增长！64 个圆盘需要移动 \\(2^{64}-1\\) 次，即使每秒移动一次，也需要约 5849 亿年。\n\\end{itemize}\n\\end{custom}",
    1,
)
first_body = first_body.replace(
    " = \\dfrac{1}{2}.\n\\]\n\\end{custom}\n\n\\begin{custom}{等价无穷小替换的口诀}",
    " = \\dfrac{1}{2}.\n\\]\n\\end{example}\n\n\\begin{custom}{等价无穷小替换的口诀}",
    1,
)
first_body = first_body.replace(
    "\\end{extra}\n\n\\end{custom}\n\n\\begin{example}\n求 \\(\\lim_{x \\to 0} \\dfrac{\\sin 2x}{x}\\)。",
    "\\end{extra}\n\n\\begin{example}\n求 \\(\\lim_{x \\to 0} \\dfrac{\\sin 2x}{x}\\)。",
    1,
)
first_body = first_body.replace(
    "\\end{enumerate}\n\\end{custom}\n\n\\clearpage\n\\section{极限的性质与重要极限}",
    "\\end{enumerate}\n\n\\clearpage\n\\section{极限的性质与重要极限}",
    1,
)
first_body = first_body.replace(
    "\\end{enumerate}\n\\end{custom}\n\n\\clearpage\n\\section{无穷级数}",
    "\\end{enumerate}\n\n\\clearpage\n\\section{无穷级数}",
    1,
)
first_body = first_body.replace(
    r"""\begin{custom}{常见错误警示}

\begin{tabular}{|c|c|c|}
\hline
\textbf{错误写法} & \textbf{问题} & \textbf{正确理解} \\
\hline
\(o(g) - o(g) = 0\) & 两个不同的 \(o(g)\) 相减不一定为 0 & \(o(g) - o(g) = o(g)\) \\
\hline
\(\dfrac{o(g)}{g} = 0\) & 写法不规范 & 应写为 \(\dfrac{o(g)}{g} \to 0\) \\
\hline
\(o(1) \cdot \infty = ?\) & 未定义 & \(o(1)\) 乘以无穷大可能为任何情况 \\
\hline
\(\sin x = x + O(x^3)\) 与 \(\sin x = x + o(x^2)\) 混淆 & 精度不同 & \(O(x^3)\) 比 \(o(x^2)\) 提供更多信息 \\
\hline
\end{tabular}
""",
    r"""\begin{custom}{常见错误警示}

\begin{center}
\small
\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}X|>{\raggedright\arraybackslash}X|>{\raggedright\arraybackslash}X|}
\hline
\textbf{错误写法} & \textbf{问题} & \textbf{正确理解} \\
\hline
\(o(g) - o(g) = 0\) & 两个不同的 \(o(g)\) 相减不一定为 0 & \(o(g) - o(g) = o(g)\) \\
\hline
\(\dfrac{o(g)}{g} = 0\) & 写法不规范 & 应写为 \(\dfrac{o(g)}{g} \to 0\) \\
\hline
\(o(1) \cdot \infty = ?\) & 未定义 & \(o(1)\) 乘以无穷大可能为任何情况 \\
\hline
\(\sin x = x + O(x^3)\) 与 \(\sin x = x + o(x^2)\) 混淆 & 精度不同 & \(O(x^3)\) 比 \(o(x^2)\) 提供更多信息 \\
\hline
\end{tabularx}
\end{center}
""",
    1,
)

arithmetic_example = r"""\begin{example}[等差数列]
若数列 $\{a_n\}$ 满足
\[
a_{n+1}-a_n=d\qquad(n=1,2,\ldots),
\]
其中 $d$ 为常数，则称 $\{a_n\}$ 为等差数列，$d$ 称为公差. 由递推式逐项相加可得
\[
a_n=a_1+(n-1)d.
\]
例如 $1,3,5,7,\ldots$ 是公差为 $2$ 的等差数列.

等差数列前 $n$ 项和为
\[
S_n=\frac{n(a_1+a_n)}{2}.
\]
证明如下：将
\[
S_n=a_1+a_2+\cdots+a_n
\]
与倒序求和式
\[
S_n=a_n+a_{n-1}+\cdots+a_1
\]
相加，得到
\[
2S_n=(a_1+a_n)+(a_2+a_{n-1})+\cdots+(a_n+a_1).
\]
每一组括号内均为 $a_1+a_n$，共有 $n$ 组，故 $2S_n=n(a_1+a_n)$.
\end{example}"""

geometric_example = r"""\begin{example}[等比数列]
若 $a_1\ne0$，且数列 $\{a_n\}$ 满足
\[
a_{n+1}=ra_n\qquad(n=1,2,\ldots),
\]
其中 $r$ 为常数，则称 $\{a_n\}$ 为等比数列，$r$ 称为公比. 由递推式可得
\[
a_n=a_1r^{\,n-1}.
\]
若 $r\ne1$，其前 $n$ 项和为
\[
S_n=a_1\frac{1-r^n}{1-r}.
\]
证明如下：由
\[
S_n=a_1+a_1r+\cdots+a_1r^{n-1}
\]
两边同乘 $r$，得
\[
rS_n=a_1r+a_1r^2+\cdots+a_1r^n.
\]
两式相减，得到 $(1-r)S_n=a_1(1-r^n)$，故上式成立. 当 $r=1$ 时，$S_n=na_1$.
\end{example}"""

first_body = re.sub(
    r"\\begin\{example\}\[等差数列\].*?\\end\{example\}",
    lambda _: arithmetic_example,
    first_body,
    count=1,
    flags=re.S,
)
first_body = re.sub(
    r"\\begin\{example\}\[等比数列\].*?\\end\{example\}",
    lambda _: geometric_example,
    first_body,
    count=1,
    flags=re.S,
)
first_body = first_body.replace(
    "希帕索斯因此被投入大海。\n\n这个故事告诉我们：有理数是不够用的。数轴上还有很多“空隙”——无理数。",
    "这一发现说明，仅使用有理数无法完整刻画几何长度。\n\n这个例子告诉我们：有理数是不够用的。数轴上还需要无理数来填补“空隙”。",
    1,
)
first_body = first_body.replace(
    "\n\\begin{custom}{参考答案提要}\n\\begin{enumerate}\n\\item[(1)]",
    "\n\\subsection*{参考答案提要}\n\\begin{custom}{参考答案提要}\n\\begin{enumerate}\n\\item[(1)]",
    1,
)
first_body = first_body.replace(
    "\n\\newpage \n\n\\begin{custom}{参考答案提要}\n\n\\begin{enumerate}\n\\item[(1)]",
    "\n\\newpage \n\n\\subsection*{参考答案提要}\n\\begin{custom}{参考答案提要}\n\n\\begin{enumerate}\n\\item[(1)]",
    1,
)
first_body = first_body.replace(
    "\n\\begin{exercise}[级数练习题]\n判断下列级数的敛散性：",
    "\n\\subsection*{练习题：无穷级数}\n\\begin{exercise}[级数练习题]\n判断下列级数的敛散性：",
    1,
)
first_body = first_body.replace(
    "\n\\begin{custom}{参考答案}\n\\begin{enumerate}\n\\item 发散（通项",
    "\n\\subsection*{参考答案：无穷级数}\n\\begin{custom}{参考答案}\n\\begin{enumerate}\n\\item 发散（通项",
    1,
)

sequence_definition_block = r"""\subsection{数列的一般定义}

从高中阶段的等差数列、等比数列出发，我们现在给出更一般也更精确的定义.

\begin{definition}[数列]
数列是定义在正整数集 $\mathbb{N}^+=\{1,2,3,\cdots\}$ 上、取实数值的函数. 若这个函数在 $n$ 处的函数值记为 $a_n$，则数列记为
\[
\{a_n\}:a_1,a_2,\ldots,a_n,\ldots .
\]
其中 $a_n$ 称为数列的第 $n$ 项或通项.
\end{definition}

这个定义说明，数列既有函数的本质，又有离散变量的特点. 函数 $y=f(x)$ 的自变量可以在区间中连续取值，而数列只在 $n=1,2,\ldots$ 这些正整数处取值. 因此，数列可以看作一种特殊函数：
\[
a_n=f(n),\qquad n\in\mathbb{N}^+.
\]
讨论数列时，项的顺序不可随意改变；同一组数字若排列顺序不同，通常就是不同数列.

\begin{example}
判断下列对象能否确定一个数列，并说明理由.
\[
(1)\ a_n=\frac{n+1}{2n-1};\qquad
(2)\ a_1=1,\ a_{n+1}=2a_n+1;\qquad
(3)\ 1,2,4,\ldots .
\]
\end{example}
\begin{custom}{解}
(1) 给出了通项公式，对每个正整数 $n$ 都能唯一确定 $a_n$，因此确定一个数列.

(2) 给出了初值和递推关系. 由 $a_1=1$ 可依次得到
\[
a_2=3,\quad a_3=7,\quad a_4=15,\ldots
\]
因此也确定一个数列.

(3) 只列出前三项，不能唯一确定一个数列. 例如 $a_n=2^{n-1}$ 的前三项为 $1,2,4$；但 $b_1=1,b_2=2,b_3=4,b_n=0(n\ge4)$ 也有同样前三项. 因此仅凭有限项通常不能严格确定无穷数列.
\end{custom}

\begin{example}
设某药物每隔固定时间给药一次，每次给药后体内新增浓度 $C_0$，两次给药之间保留比例为 $q$，其中 $0<q<1$. 若 $A_n$ 表示第 $n$ 次给药后体内药物浓度，则可建立递推模型
\[
A_{n+1}=qA_n+C_0.
\]
求该模型的稳定浓度.
\end{example}
\begin{custom}{解}
若 $A_n$ 收敛到稳定浓度 $A$，则在极限状态下应满足
\[
A=qA+C_0.
\]
解得
\[
A=\frac{C_0}{1-q}.
\]
为了说明这一步不是形式猜测，令 $B_n=A_n-A$. 由 $A=qA+C_0$ 及 $A_{n+1}=qA_n+C_0$ 得
\[
B_{n+1}=A_{n+1}-A=q(A_n-A)=qB_n.
\]
因此
\[
B_n=q^{n-1}B_1.
\]
由于 $0<q<1$，有 $q^{n-1}\to0$，所以 $B_n\to0$，即
\[
A_n\to A=\frac{C_0}{1-q}.
\]
\end{custom}

\subsection{数列的几种其他定义方式}"""

first_body = first_body.replace(
    r"""\subsection{数列的一般定义}

将高中学过的数列概念推广，我们得到数列的一般定义。

\begin{definition}[数列]
按一定次序排列的一列数称为数列，记为 \(\{a_n\}\)。其中 \(a_n\) 称为通项，\(n\) 称为下标。
\end{definition}

数列本质上是一个从正整数集 \(\mathbb{N}^*\) 到实数集 \(\mathbb{R}\) 的映射：
\[
a_n = f(n),\quad n=1,2,3,\dots
\]
数列就是“一列按顺序排好的数”。你可以想象成一条无限长的队伍，每个人都戴着一个号码牌，上面写着一个数。这个号码牌上的数，就是数列的“第 n 项”。

\subsection{数列的几种其他定义方式}""",
    sequence_definition_block,
    1,
)

limit_notes_block = r"""\subsection{数列极限的几个注解}

极限定义包含三个层次：先给定任意精度 $\varepsilon>0$，再寻找与该精度有关的正整数 $N$，最后要求所有 $n>N$ 的项同时满足误差估计. 因此，证明数列极限时不能只验证若干项接近极限，也不能只说明“越来越接近”；必须说明从某一项以后全部项都落入指定误差范围.

\begin{proposition}[极限唯一性]
若数列 $\{a_n\}$ 同时收敛于 $A$ 与 $B$，则 $A=B$.
\end{proposition}
\begin{custom}{证明}
反设 $A\ne B$，取
\[
\varepsilon=\frac{|A-B|}{3}>0.
\]
由 $a_n\to A$，存在 $N_1$，当 $n>N_1$ 时有 $|a_n-A|<\varepsilon$；由 $a_n\to B$，存在 $N_2$，当 $n>N_2$ 时有 $|a_n-B|<\varepsilon$. 取 $n>\max\{N_1,N_2\}$，则
\[
|A-B|\le |A-a_n|+|a_n-B|<2\varepsilon=\frac{2}{3}|A-B|,
\]
矛盾. 因此 $A=B$.
\end{custom}

\begin{proposition}[收敛数列有界]
若数列 $\{a_n\}$ 收敛，则 $\{a_n\}$ 有界.
\end{proposition}
\begin{custom}{证明}
设 $a_n\to A$. 取 $\varepsilon=1$，存在 $N$，当 $n>N$ 时
\[
|a_n-A|<1,
\]
从而 $|a_n|<|A|+1$. 前 $N$ 项只有有限个，令
\[
M=\max\{|a_1|,\ldots,|a_N|,|A|+1\}.
\]
则对任意正整数 $n$ 都有 $|a_n|\le M$，故数列有界.
\end{custom}

\begin{custom}{定义中的几个注意点}
\begin{enumerate}
\item 极限不要求某一项等于极限值. 例如 $a_n=1/n$ 的极限为 $0$，但每一项都不等于 $0$.
\item 极限不要求数列单调. 例如 $a_n=(-1)^n/n$ 在 $0$ 两侧交替取值，但 $|a_n|=1/n\to0$，所以 $a_n\to0$.
\item 极限要求“从某项以后全部满足”. 若一个数列有两个子列分别趋向不同的数，则原数列不可能收敛.
\end{enumerate}
\end{custom}

\subsection{用定义证明极限}"""

first_body = first_body.replace(
    r"""\subsection{数列极限的几个注解}

初学者对极限概念常有误解。下面几个注记可以帮助你更准确地理解“极限”这个词的真正含义。

\subsubsection{注一：没有一项等于极限值，也可以有极限}

很多人以为，既然极限是 \(a_n\) 趋向的那个数，那么到了某个很大的 \(n\)，\(a_n\) 就一定会等于极限值。这是不对的。

考虑数列 \(a_n = \dfrac{1}{n}\)。它的极限是 0，但你能找到一项 \(\dfrac{1}{n}\) 真正等于 0 吗？不能。不管 \(n\) 多大，\(\dfrac{1}{n}\) 永远是正数，只是越来越接近 0，但永远到不了 0。

再看数列 \(a_n = \dfrac{(-1)^n}{n}\)。它的极限也是 0，但有些项是正的（当 \(n\) 为偶数），有些项是负的（当 \(n\) 为奇数），没有一项是 0。

\textbf{结论：} 极限描述的是数列的“趋势”或“归宿”，而不是要求某项恰好等于它。就像一个不断靠近终点的人，他可以永远不踩到终点线，但我们仍然可以说他在趋近终点。

\subsubsection{注二：趋向极限的过程不一定单调，可以“左摇右摆”}

你可能从 \(\dfrac{1}{n}\) 这个例子中产生了错觉，以为数列趋近极限时应该越来越近，一路不回头。实际上不是这样。

考虑数列 \(a_n = \dfrac{(-1)^n}{n}\)：
\[
a_1 = -1,\ a_2 = 0.5,\ a_3 \approx -0.333,\ a_4 = 0.25,\ a_5 = -0.2,\ a_6 \approx 0.167,\ \dots
\]
它一会儿正，一会儿负，像醉汉走路一样左右摇晃。但摇晃的幅度越来越小——从 1 到 0.5 到 0.333 到 0.25……最终还是被“吸”向 0。

再比如 \(a_n = \dfrac{\sin n}{n}\)，它在 0 附近上下波动，但波动越来越微弱。

\textbf{结论：} 极限不要求数列单调。数列可以曲折、振荡、来回跳跃，只要最终“摇晃的幅度”趋于零，它仍然收敛。

\subsubsection{注三：等价于“极限点附近任意小的圆内，都有无穷多项”}

极限的严格定义是 \(\varepsilon\)-\(N\) 语言，但我们可以换一种更直观的说法：

\emph{如果 \(L\) 是数列的极限，那么无论你画一个多么小的圆（以 \(L\) 为中心，半径 \(\varepsilon > 0\)），这个圆内都含有数列的无穷多项（实际上是从某一项以后的所有项）。}

反过来，如果某个点附近的小圆内只含有有限多项（比如只有前几项在里面），那这个点就不是极限。

这个比喻可以帮助你直观判断：极限就是数列最终“扎堆”聚集的地方。就像一群鸟最终都落在一根树枝上——你可以选一个很小的范围，最终所有的鸟都在这个范围里。

\subsection{用定义证明极限}""",
    limit_notes_block,
    1,
)

series_concept_extension = r"""\begin{definition}[级数收敛与发散]
若部分和数列 \(\{S_n\}\) 收敛于 \(S\)，则称级数 \(\sum a_n\) 收敛，且和为 \(S\)，记作 \(\sum_{n=1}^{\infty} a_n = S\)；若 \(\{S_n\}\) 发散，则称级数发散。
\end{definition}

\begin{custom}{核心说明}
级数不是“把无穷多个数一次性相加”，而是先形成部分和数列
\[
S_1=a_1,\quad S_2=a_1+a_2,\quad \ldots,\quad S_n=a_1+\cdots+a_n,
\]
再研究 $\{S_n\}$ 是否有极限. 因此级数的敛散性完全由部分和数列决定.
\end{custom}

\begin{example}
判断级数
\[
\sum_{n=1}^{\infty}\frac{1}{n(n+1)}
\]
是否收敛，并求其和.
\end{example}
\begin{custom}{解}
先裂项：
\[
\frac{1}{n(n+1)}=\frac1n-\frac{1}{n+1}.
\]
第 $N$ 个部分和为
\[
S_N=\sum_{n=1}^{N}\left(\frac1n-\frac{1}{n+1}\right)
=1-\frac{1}{N+1}.
\]
由于 $S_N\to1$，故原级数收敛，且
\[
\sum_{n=1}^{\infty}\frac{1}{n(n+1)}=1.
\]
\end{custom}"""

first_body = first_body.replace(
    r"""\begin{definition}[级数收敛与发散]
若部分和数列 \(\{S_n\}\) 收敛于 \(S\)，则称级数 \(\sum a_n\) 收敛，且和为 \(S\)，记作 \(\sum_{n=1}^{\infty} a_n = S\)；若 \(\{S_n\}\) 发散，则称级数发散。
\end{definition}""",
    series_concept_extension,
    1,
)

def insert_after_first(text: str, marker: str, insertion: str) -> str:
    if marker not in text:
        raise ValueError(f"marker not found: {marker[:60]!r}")
    return text.replace(marker, marker + insertion, 1)


first_body = insert_after_first(
    first_body,
    r"""\begin{theorem}[单调有界准则]
单调递增且有上界的数列必收敛；单调递减且有下界的数列必收敛。
\end{theorem}""",
    r"""

\begin{custom}{证明}
只证明单调递增且有上界的情形，单调递减且有下界的情形可令 $b_n=-a_n$ 化为前一情形.

设 $\{a_n\}$ 单调递增且有上界. 由实数完备性，集合
\[
A=\{a_n:n=1,2,\ldots\}
\]
存在上确界，记为 $\alpha=\sup A$. 下面证明 $a_n\to\alpha$.

任取 $\varepsilon>0$. 因 $\alpha$ 是 $A$ 的上确界，$\alpha-\varepsilon$ 不是 $A$ 的上界，否则它会小于上确界却仍为上界，与上确界定义矛盾. 因此存在某个正整数 $N$，使得
\[
a_N>\alpha-\varepsilon.
\]
又因数列单调递增，当 $n\ge N$ 时有
\[
a_n\ge a_N>\alpha-\varepsilon.
\]
同时 $\alpha$ 是上界，故 $a_n\le \alpha$. 于是当 $n\ge N$ 时，
\[
0\le \alpha-a_n<\varepsilon,
\]
即 $|a_n-\alpha|<\varepsilon$. 由数列极限定义，$a_n\to\alpha$.
\end{custom}""",
)

first_body = insert_after_first(
    first_body,
    r"""\begin{theorem}[Bolzano-Weierstrass定理]
\textbf{（有界数列必有收敛子列）}
任何有界数列 \(\{a_n\}\) 必定存在一个收敛的子列 \(\{a_{n_k}\}\)。
\end{theorem}""",
    r"""

\begin{custom}{证明}
设 $\{a_n\}$ 有界，则存在闭区间 $I_0=[\alpha_0,\beta_0]$ 包含数列的全部项. 将 $I_0$ 等分为左右两个闭区间. 至少有一个半区间包含数列中的无穷多项；否则两个半区间都只含有限多项，合起来也只含有限多项，与原数列有无穷多项矛盾. 取其中一个含无穷多项的半区间记为 $I_1$.

继续这个过程：把 $I_{k-1}$ 等分，取一个包含数列中无穷多项的半区间 $I_k$. 得到一列闭区间
\[
I_0\supset I_1\supset I_2\supset\cdots,\qquad |I_k|=\frac{|I_0|}{2^k}.
\]
根据闭区间套定理，存在唯一实数 $\xi$ 属于所有 $I_k$，并且区间长度趋于 $0$.

下面从数列中选子列. 因 $I_1$ 含无穷多项，可取 $n_1$ 使 $a_{n_1}\in I_1$. 取定 $n_1,\ldots,n_{k-1}$ 后，由于 $I_k$ 含无穷多项，可选 $n_k>n_{k-1}$ 使 $a_{n_k}\in I_k$. 于是得到子列 $\{a_{n_k}\}$.

任取 $\varepsilon>0$. 因 $|I_k|\to0$，存在 $K$，当 $k\ge K$ 时 $|I_k|<\varepsilon$. 对 $k\ge K$，$a_{n_k}$ 与 $\xi$ 同属 $I_k$，故
\[
|a_{n_k}-\xi|\le |I_k|<\varepsilon.
\]
由极限定义，$a_{n_k}\to\xi$. 因此有界数列必有收敛子列.
\end{custom}""",
)

series_proof_insertions = [
    (
        r"""\begin{theorem}[级数的线性性质]
若级数 \(\sum_{n=1}^{\infty} a_n\) 收敛于 \(S\)，\(\sum_{n=1}^{\infty} b_n\) 收敛于 \(T\)，\(\alpha, \beta\) 为常数，则
\[
\sum_{n=1}^{\infty} (\alpha a_n + \beta b_n) = \alpha S + \beta T.
\]
\end{theorem}""",
        r"""

\begin{custom}{证明}
记
\[
A_n=\sum_{k=1}^{n}a_k,\qquad B_n=\sum_{k=1}^{n}b_k.
\]
由条件 $A_n\to S,\ B_n\to T$. 对级数 $\sum(\alpha a_n+\beta b_n)$，其第 $n$ 个部分和为
\[
\sum_{k=1}^{n}(\alpha a_k+\beta b_k)=\alpha A_n+\beta B_n.
\]
由收敛数列四则运算法则，
\[
\alpha A_n+\beta B_n\to \alpha S+\beta T.
\]
因此该级数收敛，且和为 $\alpha S+\beta T$.
\end{custom}""",
    ),
    (
        r"""\begin{theorem}[添加或删除有限项]
在级数中添加、删除或改变有限项，不改变级数的敛散性。但若级数收敛，其和可能会改变。
\end{theorem}""",
        r"""

\begin{custom}{证明}
以改变前 $m$ 项为例. 设原级数部分和为
\[
S_n=a_1+\cdots+a_n,
\]
改变前 $m$ 项后得到的新级数部分和记为 $T_n$. 当 $n>m$ 时，$T_n$ 与 $S_n$ 只相差一个固定常数 $C$，即
\[
T_n=S_n+C.
\]
若 $S_n$ 收敛，则 $T_n$ 也收敛；若 $S_n$ 发散而 $T_n$ 收敛，则 $S_n=T_n-C$ 收敛，矛盾. 因此二者敛散性相同. 当收敛时，极限值相差 $C$，所以级数和可能改变.
\end{custom}""",
    ),
    (
        r"""\begin{theorem}[加括号]
收敛级数任意加括号后所成的新级数仍然收敛，且和不变。

\textbf{注意：} 逆命题不成立。即加括号后收敛的级数，原级数未必收敛。例如：
\[
(1-1)+(1-1)+(1-1)+\cdots = 0+0+0+\cdots = 0,
\]
但原级数 \(1-1+1-1+1-1+\cdots\) 是发散的。
\end{theorem}""",
        r"""

\begin{custom}{证明}
设原级数 $\sum a_n$ 的部分和 $S_n\to S$. 任意加括号后，新级数的部分和等于原部分和数列中的一个子列：
\[
T_k=S_{n_k},\qquad 1\le n_1<n_2<\cdots .
\]
收敛数列的任意子列收敛到同一极限，因此 $T_k\to S$. 所以加括号后的级数仍收敛，且和不变. 逆命题不成立的例子如定理中所示.
\end{custom}""",
    ),
    (
        r"""\begin{theorem}[比较判别法]
设 \(\sum a_n\) 和 \(\sum b_n\) 为正项级数，且存在 \(N\)，当 \(n > N\) 时 \(a_n \leq b_n\)。
\begin{enumerate}
\item 若 \(\sum b_n\) 收敛，则 \(\sum a_n\) 收敛；
\item 若 \(\sum a_n\) 发散，则 \(\sum b_n\) 发散。
\end{enumerate}
\end{theorem}""",
        r"""

\begin{custom}{证明}
只需考虑从 $N+1$ 项开始的尾级数，因为添加或删除有限项不改变敛散性. 记
\[
A_m=\sum_{n=N+1}^{m}a_n,\qquad B_m=\sum_{n=N+1}^{m}b_n.
\]
由于 $0\le a_n\le b_n$，所以对所有 $m>N$ 有
\[
0\le A_m\le B_m.
\]
若 $\sum b_n$ 收敛，则 $\{B_m\}$ 有上界，从而 $\{A_m\}$ 是单调递增且有上界的数列，由单调有界准则知 $\{A_m\}$ 收敛，故 $\sum a_n$ 收敛.

第二个结论是第一个结论的逆否命题：若 $\sum b_n$ 收敛，则 $\sum a_n$ 收敛. 因此若 $\sum a_n$ 发散，$\sum b_n$ 不可能收敛，只能发散.
\end{custom}""",
    ),
    (
        r"""\begin{theorem}[\(p\)-级数]
\[
\sum_{n=1}^{\infty} \dfrac{1}{n^p}
\]
当 \(p > 1\) 时收敛，当 \(p \leq 1\) 时发散。
\end{theorem}""",
        r"""

\begin{custom}{证明}
先设 $p>1$. 将 $n\ge2$ 的项按
\[
2^k\le n\le 2^{k+1}-1\qquad(k=0,1,2,\ldots)
\]
分组. 在第 $k$ 组中共有 $2^k$ 项，且每项不超过 $1/(2^k)^p$，故该组和不超过
\[
2^k\cdot \frac{1}{(2^k)^p}=2^{k(1-p)}.
\]
因为 $p>1$，几何级数 $\sum_{k=0}^{\infty}2^{k(1-p)}$ 收敛，由比较判别法知 $\sum 1/n^p$ 收敛.

若 $p=1$，得到调和级数，前文已经证明其发散. 若 $p<1$，则对 $n\ge1$ 有 $n^p\le n$，从而
\[
\frac1{n^p}\ge \frac1n.
\]
由比较判别法，$\sum 1/n^p$ 发散.
\end{custom}""",
    ),
    (
        r"""\begin{theorem}[比值判别法（达朗贝尔判别法）]
设 \(\sum_{n=1}^{\infty} a_n\) 为正项级数，且 \(\lim_{n\to\infty} \dfrac{a_{n+1}}{a_n} = \rho\)，则
\begin{itemize}
\item 若 \(\rho < 1\)，级数收敛；
\item 若 \(\rho > 1\)（包括 \(\rho = +\infty\)），级数发散；
\item 若 \(\rho = 1\)，判别法失效，需用其他方法判断。
\end{itemize}
\end{theorem}""",
        r"""

\begin{custom}{证明}
若 $\rho<1$，取常数 $r$ 使 $\rho<r<1$. 由极限定义，存在 $N$，当 $n\ge N$ 时
\[
\frac{a_{n+1}}{a_n}\le r.
\]
于是
\[
a_{N+k}\le a_N r^k\qquad(k=1,2,\ldots).
\]
尾级数 $\sum_{k=1}^{\infty}a_N r^k$ 是收敛的几何级数，由比较判别法，$\sum a_n$ 收敛.

若 $\rho>1$，取 $r$ 使 $1<r<\rho$. 则存在 $N$，当 $n\ge N$ 时
\[
\frac{a_{n+1}}{a_n}\ge r>1.
\]
因此 $a_{n+1}\ge a_n$ 对充分大的 $n$ 成立，且 $a_n$ 不可能趋于 $0$. 由级数收敛的必要条件，$\sum a_n$ 发散. 当 $\rho=+\infty$ 时同理可取任意 $r>1$.

当 $\rho=1$ 时，该方法不能给出结论. 例如 $\sum 1/n$ 发散而 $\sum 1/n^2$ 收敛，二者的相邻项比值极限都为 $1$.
\end{custom}""",
    ),
    (
        r"""\begin{theorem}[根值判别法（柯西判别法）]
设 \(\sum_{n=1}^{\infty} a_n\) 为正项级数，且 \(\lim_{n\to\infty} \sqrt[n]{a_n} = \rho\)，则
\begin{itemize}
\item 若 \(\rho < 1\)，级数收敛；
\item 若 \(\rho > 1\)（包括 \(\rho = +\infty\)），级数发散；
\item 若 \(\rho = 1\)，判别法失效。
\end{itemize}
\end{theorem}""",
        r"""

\begin{custom}{证明}
若 $\rho<1$，取 $r$ 使 $\rho<r<1$. 由极限定义，存在 $N$，当 $n\ge N$ 时
\[
\sqrt[n]{a_n}\le r,
\]
即 $a_n\le r^n$. 因 $\sum r^n$ 收敛，由比较判别法知 $\sum a_n$ 收敛.

若 $\rho>1$，取 $r$ 使 $1<r<\rho$. 则存在 $N$，当 $n\ge N$ 时
\[
\sqrt[n]{a_n}\ge r,
\]
从而 $a_n\ge r^n>1$. 因此 $a_n$ 不趋于 $0$，由级数收敛的必要条件，$\sum a_n$ 发散. $\rho=+\infty$ 的情形同理.

当 $\rho=1$ 时，该判别法不能区分 $\sum 1/n$ 与 $\sum 1/n^2$ 这类情形，因此失效.
\end{custom}""",
    ),
    (
        r"""\begin{theorem}[莱布尼茨判别法]
若交错级数 \(\sum_{n=1}^{\infty} (-1)^{n-1} b_n\) 满足：
\begin{enumerate}
\item \(b_n\) 单调递减（即 \(b_1 \geq b_2 \geq b_3 \geq \cdots\)）；
\item \(\lim\limits_{n\to\infty} b_n = 0\)，
\end{enumerate}
则级数收敛，且其和 \(S\) 满足 \(0 < S < b_1\)，余项 \(|R_n| < b_{n+1}\)。
\end{theorem}""",
        r"""

\begin{custom}{证明}
记部分和为 $S_n=\sum_{k=1}^{n}(-1)^{k-1}b_k$. 偶数项部分和满足
\[
S_{2m+2}-S_{2m}=b_{2m+1}-b_{2m+2}\ge0,
\]
故 $\{S_{2m}\}$ 单调递增. 又
\[
S_{2m}=(b_1-b_2)+\cdots+(b_{2m-1}-b_{2m})\ge0,
\]
且
\[
S_{2m}=b_1-(b_2-b_3)-\cdots-(b_{2m-2}-b_{2m-1})-b_{2m}\le b_1.
\]
因此 $\{S_{2m}\}$ 单调有界，设其极限为 $S$.

奇数项部分和满足
\[
S_{2m+1}=S_{2m}+b_{2m+1}.
\]
因 $b_{2m+1}\to0$，得 $S_{2m+1}\to S$. 偶数子列和奇数子列趋于同一极限，所以 $S_n\to S$，级数收敛. 由 $0\le S_{2m}\le S\le S_{2m+1}\le b_1$ 可得 $0\le S\le b_1$；若 $b_1>0$ 且不从某项起全为零，则 $0<S<b_1$.

余项估计来自同样的夹逼. 从第 $n+1$ 项起的尾和是首项为 $b_{n+1}$、项的绝对值单调趋零的交错和，其值位于 $0$ 与首项之间或二者相反数之间，所以
\[
|R_n|\le b_{n+1}.
\]
若所有 $b_n>0$ 且严格趋向 $0$，常写为 $|R_n|<b_{n+1}$.
\end{custom}""",
    ),
    (
        r"""\begin{theorem}[绝对收敛与收敛的关系]
绝对收敛的级数一定收敛。即若 \(\sum |a_n|\) 收敛，则 \(\sum a_n\) 必收敛。
\end{theorem}""",
        r"""

\begin{custom}{证明}
定义
\[
a_n^+=\frac{|a_n|+a_n}{2},\qquad a_n^-=\frac{|a_n|-a_n}{2}.
\]
则 $a_n^+\ge0,\ a_n^-\ge0$，且
\[
a_n=a_n^+-a_n^-,\qquad 0\le a_n^+\le |a_n|,\quad 0\le a_n^-\le |a_n|.
\]
若 $\sum |a_n|$ 收敛，由比较判别法，正项级数 $\sum a_n^+$ 与 $\sum a_n^-$ 都收敛. 由级数线性性质，
\[
\sum a_n=\sum a_n^+-\sum a_n^-
\]
收敛. 因此绝对收敛必推出收敛.
\end{custom}""",
    ),
]

for marker, insertion in series_proof_insertions:
    first_body = insert_after_first(first_body, marker, insertion)

first_body = add_toc_for_starred_subsections(first_body)

# The derivative handout already had a short continuity subsection.  In the
# combined version continuity becomes an independent section, so remove the
# old subsection to avoid repetition.
old_continuity = deriv_body[
    deriv_body.index(r"\subsection{函数连续性的准备}") : deriv_body.index(
        r"\subsection{从变化率到导数}"
    )
]
deriv_body = deriv_body.replace(old_continuity, "")
deriv_body = deriv_body.replace(
    "本章的逻辑顺序如下：\n"
    "\\begin{enumerate}[label=(\\arabic*),leftmargin=2em]\n"
    "\\item 先回顾连续性，因为可导函数必连续，且许多存在性定理依赖闭区间连续函数的性质；\n"
    "\\item 再从平均变化率进入瞬时变化率，给出导数定义；\n"
    "\\item 然后解释导数的几何意义、物理意义和经济意义；\n"
    "\\item 最后通过例题说明：连续不一定可导，分段函数在衔接点处尤其需要检查左右导数.\n"
    "\\end{enumerate}",
    "本章的逻辑顺序如下：\n"
    "\\begin{enumerate}[label=(\\arabic*),leftmargin=2em]\n"
    "\\item 从平均变化率进入瞬时变化率，给出导数定义；\n"
    "\\item 解释导数的几何意义、物理意义、经济意义以及在数据建模中的意义；\n"
    "\\item 通过例题说明：连续不一定可导，分段函数在衔接点处尤其需要检查左右导数.\n"
    "\\end{enumerate}",
)


preamble = r"""%!TEX program = xelatex
\documentclass[fontset=fandol]{ctexart}
\setmainfont{Times New Roman}
\usepackage[a4paper,left=2.5cm,right=2.5cm,top=2cm,bottom=2cm]{geometry}
\usepackage{amsmath,amssymb,amsfonts,amsthm}
\usepackage{mathrsfs,bm,bbm}
\usepackage{fancyhdr}
\usepackage[colorlinks=true,linkcolor=black,citecolor=black,urlcolor=black]{hyperref}
\usepackage{enumitem}
\usepackage{booktabs,longtable,array,tabularx,multirow}
\usepackage{xparse,xstring}
\usepackage{lastpage}
\usepackage{color}
\usepackage{graphicx}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,calc,angles,positioning,shapes.geometric,graphs}
\usepackage[framemethod=TikZ]{mdframed}

\lhead{\today}
\rhead{Page \thepage\ of \pageref{LastPage}}
\cfoot{}
\setlength{\headheight}{13pt}
\pagestyle{fancy}

\mdfdefinestyle{extrastyle}{%
    linecolor=gray,
    linewidth=0.8pt,
    frametitlerule=true,
    frametitlebackgroundcolor=gray!10,
    backgroundcolor=gray!5,
    skipabove=10pt,
    skipbelow=10pt,
    innertopmargin=6pt,
    innerbottommargin=6pt
}
\newenvironment{extra}{\begin{mdframed}[style=extrastyle, frametitle={* 选读内容（不要求掌握）}]}{\end{mdframed}}

\newcounter{DefinitionCounter}[section]
\newcounter{TheoremCounter}[section]
\newcounter{PropositionCounter}[section]
\newcounter{ExampleCounter}[section]
\newcounter{ExerciseCounter}[section]
\newcounter{ProblemCounter}[section]
\newcounter{ConclusionCounter}[section]
\NewDocumentEnvironment{definition}{O{}}
{\par\noindent\refstepcounter{DefinitionCounter}\textbf{定义\theDefinitionCounter\IfStrEq{#1}{}{}{ #1}}\quad}
{\par\vspace{0.8em}}
\NewDocumentEnvironment{theorem}{O{}}
{\par\noindent\refstepcounter{TheoremCounter}\textbf{定理\theTheoremCounter\IfStrEq{#1}{}{}{ #1}}\quad}
{\par\vspace{0.8em}}
\NewDocumentEnvironment{proposition}{O{}}
{\par\noindent\refstepcounter{PropositionCounter}\textbf{性质\thePropositionCounter\IfStrEq{#1}{}{}{ #1}}\quad}
{\par\vspace{0.8em}}
\NewDocumentEnvironment{example}{O{}}
{\par\noindent\refstepcounter{ExampleCounter}\textbf{例\theExampleCounter\IfStrEq{#1}{}{}{ #1}}\quad}
{\par\vspace{0.8em}}
\NewDocumentEnvironment{exercise}{O{}}
{\par\noindent\refstepcounter{ExerciseCounter}\textbf{练习\theExerciseCounter\IfStrEq{#1}{}{}{ #1}}\quad}
{\par\vspace{0.8em}}
\NewDocumentEnvironment{problem}{O{}}
{\par\noindent\refstepcounter{ProblemCounter}\textbf{问题\theProblemCounter\IfStrEq{#1}{}{}{ #1}}\quad}
{\par\vspace{0.8em}}
\NewDocumentEnvironment{conclusion}{O{}}
{\par\noindent\refstepcounter{ConclusionCounter}\textbf{结论\theConclusionCounter\IfStrEq{#1}{}{}{ #1}}\quad}
{\par\vspace{0.8em}}
\newenvironment{custom}[1]{\par\noindent\textbf{#1}\quad}{\par\vspace{0.8em}}
\newenvironment{proofdetail}{\par\noindent\textbf{证明}\quad}{\hfill$\square$\par\vspace{0.8em}}
\newenvironment{solution}{\par\noindent\textbf{解}\quad}{\hfill$\square$\par\vspace{0.8em}}
\newenvironment{idea}{\par\noindent\textbf{思路}\quad}{\par\vspace{0.4em}}
\newenvironment{warning}{\par\noindent\textbf{易错点}\quad}{\par\vspace{0.8em}}
\newcommand{\renewEnvironmentCounter}{\setcounter{DefinitionCounter}{0}\setcounter{TheoremCounter}{0}\setcounter{PropositionCounter}{0}\setcounter{ExampleCounter}{0}\setcounter{ExerciseCounter}{0}\setcounter{ProblemCounter}{0}\setcounter{ConclusionCounter}{0}}
\newcommand{\dd}{\mathrm{d}}
\newcommand{\ee}{\mathrm{e}}
\newcommand{\RR}{\mathbbm{R}}
\newcommand{\upcite}[1]{\textsuperscript{\textsuperscript{\cite{#1}}}}
\newcommand{\bec}{\kern 0.56em\bigcirc \kern -0.85em {\small \because}\kern 0.56em}
\DeclareMathOperator*{\argmax}{\mathrm{arg\,max}}
\DeclareMathOperator*{\argmin}{\mathrm{arg\,min}}
\renewcommand{\textfraction}{0.15}
\renewcommand{\topfraction}{0.85}
\renewcommand{\bottomfraction}{0.65}
\renewcommand{\floatpagefraction}{0.60}
\renewcommand{\figurename}{图}
\renewcommand{\tablename}{表}
\setlength{\belowcaptionskip}{4pt}
\setlength{\abovecaptionskip}{4pt}

\title{大学数学I讲义\\完整合并版}
\author{数学科学学院课程讲义草稿}
\date{\today}

\begin{document}
\maketitle
\vspace{-1em}

\renewcommand{\contentsname}{\hspace*{\fill}\Large\bfseries 目\quad 录 \hspace*{\fill}}
\setcounter{tocdepth}{2}
\tableofcontents
\clearpage
"""


history_section = r"""
\section{数学文化与数学史导引}
\renewEnvironmentCounter

这一节供课下阅读. 它不要求大家记忆年代和人名，而希望帮助大家看到：数学并不是孤立公式的堆积，而是在长期解决问题的过程中形成的一套语言. 一个数学概念通常经历三步：先在实际问题中反复出现，再被抽象为稳定对象，最后被放入由定义、定理和证明组成的逻辑系统. 本讲义后面使用“定义--定理--证明--例题”的写法，正是为了让计算有根据，让应用有边界.

\subsection{河谷文明：从测量和记账到算法}

数学最初常常从实际需要中生长出来. 尼罗河泛滥后要重新丈量土地，粮食征收和工程建设需要稳定的计算规则，天文观测和历法编制需要处理周期. 因此，早期数学首先表现为算法：给出一套可重复执行的步骤，使不同的人在相同数据下得到相同结果.

古埃及纸草书中保存了分数、面积和体积计算的题目；美索不达米亚泥板中可以看到二次方程、倒数表和与勾股数组有关的材料. 这些内容的共同特征是重视“怎样算”. 例如计算一块田地面积时，真实田地可能边界不规则，数学处理会先把它近似成三角形、梯形或若干简单图形的组合，再用可操作的规则求面积. 这里已经有建模思想：现实对象先被简化为数学对象，然后才进入计算.

本课程开头学习数列，也可以从这种算法传统理解. 数列描述按步骤产生的量，例如人口逐期增长、药物多次给药后的浓度、贷款余额的递推变化. 极限则回答更深的问题：当步骤无限继续时，某个量是否趋于稳定？这个问题不能只靠观察前几项回答，所以需要 $\varepsilon$--$N$ 语言来规定“最终稳定”的精确含义.

\subsection{希腊数学：证明为什么成为数学的核心}

如果说早期算法回答“怎样算”，那么古希腊数学突出追问“为什么一定对”. 欧几里得的《几何原本》把几何知识组织成定义、公设、公理、命题和证明. 这种写法的意义在于：一旦承认起点和推理规则，后续结论就不再依赖画图是否准确，也不依赖某个例子是否看起来成立.\footnote{关于欧几里得的生平与《几何原本》的影响，可参见 MacTutor: \url{https://mathshistory.st-andrews.ac.uk/Biographies/Euclid/}.}

一个典型例子是 $\sqrt2$ 的无理性. 在边长为 $1$ 的正方形中，对角线长度满足 $d^2=2$. 若假设 $d=\frac pq$ 为既约分数，则
\[
p^2=2q^2.
\]
于是 $p^2$ 为偶数，故 $p$ 为偶数，设 $p=2k$. 代回得
\[
4k^2=2q^2,\qquad q^2=2k^2,
\]
所以 $q$ 也为偶数. 这与 $\frac pq$ 既约矛盾. 因此 $\sqrt2$ 不是有理数. 这个证明很短，却说明了一个深刻事实：数轴上仅有有理数并不够，几何长度会迫使我们扩充数系.

阿基米德在面积和体积问题中进一步发展了逼近思想. 他用内接和外切多边形估计圆周率，也用类似穷竭法的思想研究抛物线弓形面积、球的体积和表面积.\footnote{关于阿基米德及其穷竭法思想，可参见 MacTutor: \url{https://mathshistory.st-andrews.ac.uk/Biographies/Archimedes/}.} 这些工作虽然还没有现代极限符号，却已经非常接近本课程中的核心观念：用一列越来越精细的近似对象夹住目标量，并证明误差可以任意小.

阿波罗尼奥斯系统研究圆锥曲线，给出了椭圆、抛物线、双曲线等对象的几何理论.\footnote{关于阿波罗尼奥斯和圆锥曲线，可参见 MacTutor: \url{https://mathshistory.st-andrews.ac.uk/Biographies/Apollonius/}.} 后来解析几何把这些曲线写成方程，微积分又研究这些曲线的切线、面积和极值. 从几何图形到代数方程，再到导数和积分，这是数学语言逐层精密化的过程.

\subsection{中国古代数学：问题集、算法与逼近}

中国古代数学很重视“问题--算法--校验”的传统. 《九章算术》以问题集方式组织材料，内容涉及面积体积、比例分配、工程计算、线性方程组和勾股问题. 例如“方程”章用算筹排列未知量系数，本质上是在处理线性方程组；这种列阵计算与今天线性代数中的消元法有明显联系.\footnote{关于中国数学传统，可参见 MacTutor 的 Chinese mathematics overview: \url{https://mathshistory.st-andrews.ac.uk/HistTopics/Chinese_overview/}.}

刘徽为《九章算术》作注时，不满足于只给算法，而是说明算法成立的理由. 他的割圆术是极限思想的一个重要历史实例：用圆内接正多边形的面积逼近圆面积，边数越多，多边形越接近圆. 若用现代语言表达，就是构造一列近似值，并研究它们是否趋向一个确定的量. 这与后来用数列极限定义圆周率、面积和积分有共同精神.

祖冲之父子在圆周率计算上给出了很精确的结果；孙子算经中有后来被称为“中国剩余定理”的同余问题；秦九韶在《数书九章》中给出多项式求值方法，现代常称为秦九韶算法. 这些例子说明，中国数学并不只是“算术技巧”，其中包含算法复杂度、误差控制和结构化计算的雏形. 对今天学习数学的学生来说，这一传统很有启发：严谨证明保证结论可靠，算法实现保证方法可以落地.

\subsection{变化的语言：微积分}

微积分的形成，是因为人们需要同时处理两类问题：一类是瞬时变化，例如速度、切线斜率、边际成本；另一类是累积总量，例如面积、路程、总收益. 费马研究曲线切线和极值，笛卡尔把几何问题转化为代数方程，牛顿从运动和力学出发发展“流数法”，莱布尼茨则形成了影响深远的微分符号 $\dd x,\dd y$ 和积分符号 $\int$.\footnote{关于微积分兴起的历史脉络，可参见 MacTutor: The rise of calculus, \url{https://mathshistory.st-andrews.ac.uk/HistTopics/The_rise_of_calculus/}.}

以切线问题为例，割线斜率为
\[
\frac{f(x+\Delta x)-f(x)}{\Delta x}.
\]
当 $\Delta x$ 趋于 $0$ 时，如果这个比值趋于确定数，就得到切线斜率，也就是导数. 以面积问题为例，把曲边图形切成许多窄条并求和，窄条越细，总和越接近真实面积. 这两类问题表面上一个求局部变化，一个求整体累积，但微积分基本定理揭示了它们之间的内在联系.

本讲义后半部分的导数、中值定理和 Taylor 公式都属于这条主线. 导数把“局部变化”变成极限；中值定理说明局部变化率与整体变化之间存在严格联系；Taylor 公式则告诉我们，在适当条件下，复杂函数可以用多项式近似. 这些内容在经济学中的边际分析、管理学中的优化问题、医学中的剂量反应模型、机器学习中的损失函数最小化中都会反复出现.

\subsection{严谨化：从直觉无穷小到极限语言}

早期微积分大量使用“无穷小量”的直觉，这使计算非常有效，但也带来逻辑困难：无穷小既像不是零，又常常在计算中被忽略. 十九世纪以后，柯西、魏尔斯特拉斯等人用极限语言重建微积分基础. 今天我们说
\[
\lim_{x\to x_0}f(x)=A,
\]
不是说 $x$ 真的“到达” $x_0$，而是说只要允许误差足够小，就能找到相应的邻域，使函数值落入指定误差范围. 这正是 $\varepsilon$--$\delta$ 或 $\varepsilon$--$N$ 语言的作用.

因此，严格性并不是把简单问题变复杂，而是在处理“无限逼近”“瞬时变化”“无穷求和”时避免误判. 例如从前几项看起来趋近某数，并不能证明数列收敛；图像看起来有切线，也不能替代导数存在的验证；通项趋于零，也不能保证级数收敛. 这些都是本课程反复强调定义和定理条件的原因.

\subsection{从计算机到人工智能}

二十世纪以来，数学与计算机科学相互推动. 算法需要离散数学、极限估计和误差控制；数据建模需要概率统计、线性代数和优化理论；人工智能中的许多训练过程，本质上是在高维参数空间中寻找使损失函数变小的方向.\footnote{关于人工智能的概念与历史背景，可参见 Stanford Encyclopedia of Philosophy, Artificial Intelligence: \url{https://plato.stanford.edu/entries/artificial-intelligence/}.}

例如梯度下降法的基本形式为
\[
\theta_{k+1}=\theta_k-\eta\nabla L(\theta_k),
\]
其中 $L$ 是损失函数，$\nabla L$ 是梯度，$\eta$ 是学习率. 这个公式背后正是导数的含义：导数或偏导数描述函数沿某个方向变化的快慢，负梯度方向通常给出局部下降最快的方向. 在线性回归中，损失函数常取
\[
L(w,b)=\frac1m\sum_{i=1}^m(wx_i+b-y_i)^2.
\]
训练模型就是调节 $w,b$，使预测值 $wx_i+b$ 尽量接近观测值 $y_i$. 求导告诉我们 $w,b$ 应向哪个方向改动；凸性则帮助判断是否会陷入局部极小. 因此，学习导数不是只为了画切线，也是在学习现代优化算法的基础语言.

\subsection{一条贯穿本课程的线索}

可以把本课程看成三次递进. 第一，极限把“无限过程”纳入严格讨论：数列是否稳定，函数是否趋近某值，级数是否收敛. 第二，连续与导数把“变化”变成可计算对象：函数图像是否断裂，瞬时变化率是否存在，局部信息能否推出整体结论. 第三，微分和 Taylor 公式把“近似”变成有控制的工具：在误差可估计的前提下，用简单表达式代替复杂表达式.

斐波那契数列可以作为一个小例子贯穿这三层. 它由递推关系
\[
a_{n+2}=a_{n+1}+a_n
\]
给出，体现“按步骤生成”的思想；相邻两项比值若收敛，则极限 $r$ 满足
\[
r=1+\frac1r,
\]
从而得到黄金分割数
\[
r=\frac{1+\sqrt5}{2}.
\]
这里既有递推，也有极限，还有从具体数列抽象出稳定比例的过程.\footnote{关于 Fibonacci 数列和黄金分割的基本事实，可参见 Wolfram MathWorld, Fibonacci Number: \url{https://mathworld.wolfram.com/FibonacciNumber.html}.}
"""


rigor_section = r"""
\section{数列、极限与级数的严谨化补充}
\renewEnvironmentCounter

本节作为前半部分内容的严谨性补充，目的不是替代后面各节，而是先把几个反复使用的逻辑支点说明清楚：数列是什么，极限定义中的 $\varepsilon$ 与 $N$ 怎样配合，为什么收敛数列有唯一极限，为什么单调有界数列一定收敛，以及级数收敛本质上是在讨论部分和数列的极限.

\subsection{数列是定义在正整数集上的函数}

\begin{definition}[数列]
数列是定义在正整数集 $\mathbb{N}^+=\{1,2,3,\cdots\}$ 上、取实数值的函数. 若第 $n$ 项记为 $a_n$，则数列记为 $\{a_n\}$.
\end{definition}

这个定义强调两点. 第一，数列有顺序，$a_1,a_2,\ldots$ 不能任意交换；第二，数列可以由通项公式、递推式、列表或实际问题共同确定. 例如 $a_n=\frac1n$ 给出通项公式，而 $a_{n+1}=0.8a_n+5$ 给出递推关系，后者常用于描述具有“保留一部分旧状态并加入新输入”的过程.

\begin{example}
设药物每隔固定时间给药一次，每次给药后体内新增浓度 $C_0$，两次给药之间保留比例为 $q$，其中 $0<q<1$. 若 $A_n$ 表示第 $n$ 次给药后浓度，则
\[
A_{n+1}=qA_n+C_0.
\]
求其平衡浓度.
\end{example}
\begin{solution}
若浓度趋于平衡值 $A$，则极限应满足
\[
A=qA+C_0.
\]
因此
\[
A=\frac{C_0}{1-q}.
\]
严格地说，令 $B_n=A_n-A$，由递推式得
\[
B_{n+1}=qB_n,
\]
故 $B_n=q^{n-1}B_1\to0$. 因而 $A_n\to A=\frac{C_0}{1-q}$.
\end{solution}

\subsection{数列极限的逻辑结构}

\begin{definition}[数列极限]
设 $\{a_n\}$ 为数列，$A$ 为实数. 若对任意 $\varepsilon>0$，存在正整数 $N$，使得当 $n>N$ 时都有
\[
|a_n-A|<\varepsilon,
\]
则称数列 $\{a_n\}$ 收敛于 $A$，记作
\[
\lim_{n\to\infty}a_n=A.
\]
\end{definition}

定义中的 $\varepsilon$ 表示允许误差，$N$ 表示从第几项以后进入并永远停留在误差范围内. $N$ 可以依赖 $\varepsilon$，但不能依赖 $n$.

\begin{example}
用定义证明 $\lim_{n\to\infty}\frac{2n+1}{n}=2$.
\end{example}
\begin{solution}
有
\[
\left|\frac{2n+1}{n}-2\right|=\frac1n.
\]
给定任意 $\varepsilon>0$，取正整数 $N>\frac1\varepsilon$. 当 $n>N$ 时，
\[
\left|\frac{2n+1}{n}-2\right|=\frac1n<\frac1N<\varepsilon.
\]
由数列极限定义，结论成立.
\end{solution}

\begin{theorem}[极限唯一性]
若数列 $\{a_n\}$ 同时收敛于 $A$ 与 $B$，则 $A=B$.
\end{theorem}
\begin{proofdetail}
反设 $A\neq B$，令 $\varepsilon=\frac{|A-B|}{3}>0$. 因 $a_n\to A$，存在 $N_1$，当 $n>N_1$ 时 $|a_n-A|<\varepsilon$；因 $a_n\to B$，存在 $N_2$，当 $n>N_2$ 时 $|a_n-B|<\varepsilon$. 取 $n>\max\{N_1,N_2\}$，由三角不等式
\[
|A-B|\le |A-a_n|+|a_n-B|<2\varepsilon=\frac{2}{3}|A-B|,
\]
矛盾. 故 $A=B$.
\end{proofdetail}

\begin{theorem}[收敛数列有界]
若数列 $\{a_n\}$ 收敛，则 $\{a_n\}$ 有界.
\end{theorem}
\begin{proofdetail}
设 $a_n\to A$. 取 $\varepsilon=1$，存在 $N$，当 $n>N$ 时
\[
|a_n-A|<1,
\]
于是 $|a_n|<|A|+1$. 前 $N$ 项只有有限个，令
\[
M=\max\{|a_1|,\ldots,|a_N|,|A|+1\},
\]
则对所有正整数 $n$ 都有 $|a_n|\le M$. 因此数列有界.
\end{proofdetail}

\begin{theorem}[夹逼准则]
若存在正整数 $N_0$，使得当 $n>N_0$ 时
\[
b_n\le a_n\le c_n,
\]
且 $\lim_{n\to\infty}b_n=\lim_{n\to\infty}c_n=A$，则 $\lim_{n\to\infty}a_n=A$.
\end{theorem}
\begin{proofdetail}
给定任意 $\varepsilon>0$. 因 $b_n\to A$，存在 $N_1$，当 $n>N_1$ 时 $A-\varepsilon<b_n<A+\varepsilon$；因 $c_n\to A$，存在 $N_2$，当 $n>N_2$ 时 $A-\varepsilon<c_n<A+\varepsilon$. 取
\[
N=\max\{N_0,N_1,N_2\}.
\]
当 $n>N$ 时，
\[
A-\varepsilon<b_n\le a_n\le c_n<A+\varepsilon,
\]
故 $|a_n-A|<\varepsilon$. 由定义得 $a_n\to A$.
\end{proofdetail}

\subsection{单调有界准则与级数}

\begin{theorem}[单调有界准则]
若数列 $\{a_n\}$ 单调递增且有上界，则 $\{a_n\}$ 收敛. 若数列单调递减且有下界，则 $\{a_n\}$ 收敛.
\end{theorem}
\begin{proofdetail}
只证单调递增且有上界的情形. 令
\[
A=\sup\{a_n:n\in\mathbb{N}^+\}.
\]
由上确界定义，对任意 $\varepsilon>0$，存在某一项 $a_N$，使得
\[
A-\varepsilon<a_N\le A.
\]
当 $n>N$ 时，由单调递增性 $a_n\ge a_N$，同时由 $A$ 是上界 $a_n\le A$. 因此
\[
A-\varepsilon<a_n\le A<A+\varepsilon,
\]
即 $|a_n-A|<\varepsilon$. 故 $a_n\to A$. 单调递减有下界情形可对 $-a_n$ 应用已证结论.
\end{proofdetail}

\begin{definition}[无穷级数与部分和]
给定数列 $\{u_n\}$，形式和
\[
\sum_{n=1}^{\infty}u_n
\]
称为无穷级数. 其第 $N$ 个部分和定义为
\[
S_N=\sum_{n=1}^{N}u_n.
\]
若部分和数列 $\{S_N\}$ 收敛，则称级数收敛；若 $\{S_N\}$ 发散，则称级数发散.
\end{definition}

\begin{example}
求几何级数 $\sum_{n=0}^{\infty}ar^n$ 的敛散性与和.
\end{example}
\begin{solution}
当 $r\neq1$ 时，部分和为
\[
S_N=a+ar+\cdots+ar^N=a\frac{1-r^{N+1}}{1-r}.
\]
若 $|r|<1$，则 $r^{N+1}\to0$，所以
\[
\sum_{n=0}^{\infty}ar^n=\lim_{N\to\infty}S_N=\frac{a}{1-r}.
\]
若 $|r|\ge1$，通项 $ar^n$ 一般不趋于 $0$；当 $a\neq0$ 时级数发散. 若 $a=0$，级数每项为 $0$，收敛且和为 $0$.
\end{solution}

\begin{warning}
级数收敛必须检查部分和数列，而不能只凭“项越来越小”判断. 例如调和级数 $\sum_{n=1}^{\infty}\frac1n$ 的通项趋于 $0$，但级数发散.
\end{warning}
"""


continuity_section = r"""
\section{函数连续性}
\renewEnvironmentCounter

连续性连接了极限与导数. 直观地说，函数在一点连续表示当自变量发生足够小的变化时，函数值也只发生足够小的变化；几何上表现为图像在该点没有跳跃、空洞或爆裂. 但在大学数学中，仅靠图像直观是不够的，连续性必须由极限严格定义.

\subsection{一点连续、左右连续与区间连续}

\begin{definition}[函数在一点连续]
设函数 $f$ 在点 $x_0$ 的某邻域内有定义，且 $f(x_0)$ 有定义. 若
\[
\lim_{x\to x_0}f(x)=f(x_0),
\]
则称 $f$ 在点 $x_0$ 处连续. 等价地，对任意 $\varepsilon>0$，存在 $\delta>0$，使得当 $|x-x_0|<\delta$ 且 $x$ 属于函数定义域时，都有
\[
|f(x)-f(x_0)|<\varepsilon.
\]
\end{definition}

\begin{definition}[左右连续]
若
\[
\lim_{x\to x_0-}f(x)=f(x_0),
\]
则称 $f$ 在 $x_0$ 处左连续；若
\[
\lim_{x\to x_0+}f(x)=f(x_0),
\]
则称 $f$ 在 $x_0$ 处右连续. 函数在 $x_0$ 连续，当且仅当它在 $x_0$ 左连续且右连续.
\end{definition}

\begin{definition}[区间上的连续]
若 $f$ 在开区间 $(a,b)$ 内每一点连续，则称 $f$ 在 $(a,b)$ 上连续. 若 $f$ 在 $(a,b)$ 内连续，且
\[
\lim_{x\to a+}f(x)=f(a),\qquad \lim_{x\to b-}f(x)=f(b),
\]
则称 $f$ 在闭区间 $[a,b]$ 上连续.
\end{definition}

\begin{center}
\begin{tikzpicture}[scale=0.9,>=Stealth]
  \draw[->] (-0.3,0)--(5.8,0) node[right] {$x$};
  \draw[->] (0,-0.3)--(0,3.2) node[above] {$y$};
  \draw[domain=0.3:5.2,smooth,variable=\x,thick] plot ({\x},{1.4+0.35*sin(80*\x)});
  \node at (2.9,-0.55) {连续图像：局部变化不会出现跳跃};
\end{tikzpicture}
\qquad
\begin{tikzpicture}[scale=0.9,>=Stealth]
  \draw[->] (-0.3,0)--(5.8,0) node[right] {$x$};
  \draw[->] (0,-0.3)--(0,3.2) node[above] {$y$};
  \draw[domain=0.3:2.65,smooth,variable=\x,thick] plot ({\x},{0.7+0.25*\x});
  \draw[domain=2.75:5.2,smooth,variable=\x,thick] plot ({\x},{1.8+0.12*(\x-3)^2});
  \filldraw[white] (2.7,1.375) circle (2.2pt);
  \draw (2.7,1.375) circle (2.2pt);
  \fill (2.7,1.81) circle (2.2pt);
  \node at (2.9,-0.55) {不连续图像：极限值与函数值不一致};
\end{tikzpicture}
\end{center}

\subsection{连续函数的运算性质}

\begin{proposition}[四则运算]
若 $f,g$ 在 $x_0$ 处连续，则 $f+g,\,f-g,\,fg$ 在 $x_0$ 处连续. 若 $g(x_0)\neq0$，则 $\frac{f}{g}$ 在 $x_0$ 处连续.
\end{proposition}
\begin{proofdetail}
以乘积为例. 由连续性得
\[
\lim_{x\to x_0}f(x)=f(x_0),\qquad \lim_{x\to x_0}g(x)=g(x_0).
\]
由极限乘法法则，
\[
\lim_{x\to x_0}f(x)g(x)=f(x_0)g(x_0),
\]
故 $fg$ 在 $x_0$ 连续. 加、减同理. 对商函数，由 $g(x_0)\neq0$ 且 $g$ 连续，存在 $x_0$ 的某邻域使 $g(x)\neq0$，于是商函数在该邻域有定义，并由极限商法则得
\[
\lim_{x\to x_0}\frac{f(x)}{g(x)}=\frac{f(x_0)}{g(x_0)}.
\]
故 $\frac{f}{g}$ 连续.
\end{proofdetail}

\begin{proposition}[复合函数连续性]
若 $g$ 在 $x_0$ 处连续，$f$ 在 $g(x_0)$ 处连续，则复合函数 $f\circ g$ 在 $x_0$ 处连续.
\end{proposition}
\begin{proofdetail}
记 $y_0=g(x_0)$. 给定任意 $\varepsilon>0$. 因 $f$ 在 $y_0$ 处连续，存在 $\eta>0$，使得当 $|y-y_0|<\eta$ 时，
\[
|f(y)-f(y_0)|<\varepsilon.
\]
因 $g$ 在 $x_0$ 处连续，存在 $\delta>0$，使得当 $|x-x_0|<\delta$ 时，
\[
|g(x)-g(x_0)|<\eta.
\]
于是当 $|x-x_0|<\delta$ 时，
\[
|f(g(x))-f(g(x_0))|<\varepsilon.
\]
这正是 $f\circ g$ 在 $x_0$ 处连续.
\end{proofdetail}

\subsection{间断点及其判断}

\begin{definition}[间断点]
若 $f$ 在 $x_0$ 不连续，则称 $x_0$ 为 $f$ 的间断点. 常见情形包括：
\begin{enumerate}[label=(\arabic*),leftmargin=2em]
\item 可去间断：$\lim_{x\to x_0}f(x)$ 存在，但不等于 $f(x_0)$，或 $f(x_0)$ 未定义；
\item 跳跃间断：左右极限都存在但不相等；
\item 无穷间断：函数值在该点附近趋于无穷大或无穷小；
\item 振荡间断：函数在该点附近无限振荡，极限不存在.
\end{enumerate}
\end{definition}

\begin{example}
讨论函数
\[
f(x)=
\begin{cases}
\dfrac{\sin x}{x},&x\neq0,\\
a,&x=0
\end{cases}
\]
在 $x=0$ 处的连续性.
\end{example}
\begin{solution}
因为
\[
\lim_{x\to0}\frac{\sin x}{x}=1,
\]
所以 $f$ 在 $0$ 处连续当且仅当 $a=1$. 若 $a\neq1$，极限存在但不等于函数值，$0$ 是可去间断点.
\end{solution}
\begin{warning}
分段函数在分段点处必须检查左极限、右极限和函数值三者. 只检查表达式能否代入，不能保证连续.
\end{warning}

\begin{example}
设
\[
f(x)=
\begin{cases}
x^2+1,&x<1,\\
ax+b,&x\ge1.
\end{cases}
\]
求 $a,b$ 的条件，使 $f$ 在 $x=1$ 连续；若还要求左右导数相等，求 $a,b$.
\end{example}
\begin{solution}
连续要求
\[
\lim_{x\to1-}f(x)=f(1).
\]
左极限为 $2$，右侧函数值 $f(1)=a+b$，故连续条件为
\[
a+b=2.
\]
若还要求左右导数相等，左侧导数为 $(x^2+1)'|_{x=1}=2$，右侧导数为 $a$，故 $a=2$. 代入连续条件得 $b=0$.
\end{solution}

\subsection{闭区间连续函数的两个基本定理}

\begin{theorem}[有界性与最值定理]
若 $f$ 在闭区间 $[a,b]$ 上连续，则 $f$ 在 $[a,b]$ 上有界，并且存在 $x_m,x_M\in[a,b]$，使得
\[
f(x_m)\le f(x)\le f(x_M)\qquad (x\in[a,b]).
\]
\end{theorem}
\begin{proofdetail}
先证有界性. 若 $f$ 无界，则对每个正整数 $n$，可取 $x_n\in[a,b]$ 使 $|f(x_n)|>n$. 数列 $\{x_n\}$ 有界，故存在收敛子列 $x_{n_k}\to x_0\in[a,b]$. 由于 $f$ 在 $x_0$ 连续，有 $f(x_{n_k})\to f(x_0)$，于是 $\{f(x_{n_k})\}$ 有界. 但 $|f(x_{n_k})|>n_k\to\infty$，矛盾. 故 $f$ 有界.

设
\[
M=\sup\{f(x):x\in[a,b]\}.
\]
由上确界定义，对每个 $n$ 存在 $x_n\in[a,b]$，使
\[
M-\frac1n<f(x_n)\le M.
\]
取收敛子列 $x_{n_k}\to x_M\in[a,b]$. 连续性给出
\[
f(x_M)=\lim_{k\to\infty}f(x_{n_k})=M.
\]
故最大值取到. 对 $-f$ 应用同样结论，可得最小值取到.
\end{proofdetail}

\begin{theorem}[介值定理]
若 $f$ 在 $[a,b]$ 上连续，且 $N$ 介于 $f(a)$ 与 $f(b)$ 之间，则存在 $\xi\in[a,b]$，使得
\[
f(\xi)=N.
\]
\end{theorem}
\begin{proofdetail}
不妨设 $f(a)<N<f(b)$. 令
\[
S=\{x\in[a,b]:f(x)<N\}.
\]
则 $S$ 非空且有上界. 设 $\xi=\sup S$. 若 $f(\xi)>N$，由连续性可得 $\xi$ 左侧足够近的点也满足 $f(x)>N$，这与 $\xi$ 是 $S$ 的上确界矛盾. 若 $f(\xi)<N$，由连续性可得 $\xi$ 右侧足够近的点仍满足 $f(x)<N$，这与 $\xi$ 是 $S$ 的上界矛盾；若 $\xi=b$，则与 $f(b)>N$ 矛盾. 因此只能有 $f(\xi)=N$.
\end{proofdetail}

\begin{example}
证明方程 $x^3+x-1=0$ 在 $(0,1)$ 内至少有一个实根.
\end{example}
\begin{solution}
令 $f(x)=x^3+x-1$. 多项式函数在 $[0,1]$ 上连续. 有
\[
f(0)=-1,\qquad f(1)=1.
\]
由于 $0$ 介于 $f(0)$ 与 $f(1)$ 之间，由介值定理，存在 $\xi\in(0,1)$，使 $f(\xi)=0$. 因而方程在 $(0,1)$ 内至少有一个实根.
\end{solution}

\begin{example}
某商品价格为 $p$ 时的需求量模型为 $Q(p)=120-5p$，其中 $p$ 的单位为元，$Q$ 的单位为件. 若价格从 $12$ 元连续调整到 $20$ 元，问是否存在某个价格使需求量恰好为 $40$ 件？
\end{example}
\begin{solution}
这里的“需求函数” $Q(p)$ 表示价格 $p$ 与消费者愿意购买数量之间的函数关系. 模型 $Q(p)=120-5p$ 为一次函数，因此在 $[12,20]$ 上连续. 有
\[
Q(12)=60,\qquad Q(20)=20.
\]
由于 $40$ 介于 $20$ 与 $60$ 之间，介值定理保证存在 $\xi\in[12,20]$，使 $Q(\xi)=40$. 直接求解 $120-5\xi=40$，得 $\xi=16$.
\end{solution}

\subsection{课后习题}
\begin{enumerate}[label=\textbf{练习\arabic*.},leftmargin=2.2em]
\item 求常数 $a$，使
\[
f(x)=
\begin{cases}
\dfrac{1-\cos x}{x^2},&x\neq0,\\
a,&x=0
\end{cases}
\]
在 $x=0$ 连续.
\item 讨论函数 $f(x)=\frac{x^2-1}{x-1}$ 在 $x=1$ 处的间断类型，并说明如何补充定义使其连续.
\item 证明方程 $\cos x=x$ 在 $(0,1)$ 内至少有一个实根.
\item 设成本函数 $C(x)=100+20x+0.5x^2$，价格函数 $p(x)=80-0.2x$. 若收益 $R(x)=xp(x)$，利润 $P(x)=R(x)-C(x)$，说明 $P$ 在 $[0,100]$ 上是否一定能取到最大值.
\end{enumerate}

\subsection{参考解答}
\begin{enumerate}[label=\textbf{练习\arabic*.},leftmargin=2.2em]
\item 因 $\lim_{x\to0}\frac{1-\cos x}{x^2}=\frac12$，故 $a=\frac12$.
\item 当 $x\neq1$ 时 $f(x)=x+1$，故 $\lim_{x\to1}f(x)=2$，但原函数在 $x=1$ 未定义. 这是可去间断点. 定义 $f(1)=2$ 后函数在 $x=1$ 连续.
\item 令 $F(x)=\cos x-x$. $F$ 在 $[0,1]$ 上连续，且 $F(0)=1>0$，$F(1)=\cos1-1<0$. 由介值定理，存在 $\xi\in(0,1)$ 使 $F(\xi)=0$.
\item $P(x)=x(80-0.2x)-(100+20x+0.5x^2)$ 是多项式函数，故在 $[0,100]$ 上连续. 由闭区间连续函数最值定理，$P$ 在 $[0,100]$ 上一定能取到最大值和最小值.
\end{enumerate}
"""


gradient_block = r"""
\subsection{导数与梯度下降的基本思想}

导数还可以解释机器学习中最常见的优化步骤. 在监督学习中，模型含有参数，训练的目标通常是让损失函数尽量小. 损失函数衡量预测值与真实值之间的差距；例如一元线性模型 $\hat y=wx$ 对单个样本 $(x,y)$ 的平方损失可以写成
\[
L(w)=\frac12(wx-y)^2.
\]
这里 $w$ 是待学习参数，$L(w)$ 是关于参数的函数. 若 $L'(w)>0$，则在 $w$ 附近增大 $w$ 会使损失增大，减小 $w$ 有助于降低损失；若 $L'(w)<0$，则增大 $w$ 有助于降低损失. 因此，一维梯度下降更新为
\[
w_{k+1}=w_k-\eta L'(w_k),
\]
其中 $\eta>0$ 称为学习率.

\begin{example}
设损失函数 $L(w)=\frac12(w-3)^2$. 用梯度下降
\[
w_{k+1}=w_k-\eta L'(w_k)
\]
讨论 $0<\eta<2$ 时 $w_k$ 是否收敛到最小点.
\end{example}
\begin{solution}
先求导：
\[
L'(w)=w-3.
\]
因此
\[
w_{k+1}=w_k-\eta(w_k-3)=(1-\eta)w_k+3\eta.
\]
两边同时减去 $3$，得
\[
w_{k+1}-3=(1-\eta)(w_k-3).
\]
递推得到
\[
w_k-3=(1-\eta)^k(w_0-3).
\]
当 $0<\eta<2$ 时，$|1-\eta|<1$，所以 $(1-\eta)^k\to0$，于是 $w_k\to3$. 这说明学习率过大可能破坏收敛，而合适的学习率使参数逐步靠近损失函数的最小点.
\end{solution}
\begin{warning}
梯度下降中的“梯度”不是神秘操作. 在一元函数中它就是导数；在多元函数中它由各偏导数组成. 本节先理解一元导数，后面学习偏导数与全微分时会给出多参数模型的计算.
\end{warning}
"""


multi_ml_block = r"""
\subsection{偏导数在多参数机器学习模型中的应用}

多元函数的偏导数可以直接解释多参数模型训练. 设有 $m$ 个样本 $(x_i,y_i)$，用一元线性模型
\[
\hat y_i=wx_i+b
\]
进行预测. 常用的均方误差损失为
\[
J(w,b)=\frac{1}{2m}\sum_{i=1}^{m}(wx_i+b-y_i)^2.
\]
这里 $J$ 是关于两个变量 $w,b$ 的函数. 对 $w$ 和 $b$ 分别求偏导，得
\[
\frac{\partial J}{\partial w}
=\frac{1}{m}\sum_{i=1}^{m}(wx_i+b-y_i)x_i,
\qquad
\frac{\partial J}{\partial b}
=\frac{1}{m}\sum_{i=1}^{m}(wx_i+b-y_i).
\]
梯度下降更新为
\[
w_{k+1}=w_k-\eta\frac{\partial J}{\partial w}(w_k,b_k),\qquad
b_{k+1}=b_k-\eta\frac{\partial J}{\partial b}(w_k,b_k).
\]

\begin{example}
对两个样本 $(1,2),(2,3)$，写出线性模型 $\hat y=wx+b$ 的损失函数，并求 $\nabla J(0,0)$.
\end{example}
\begin{solution}
此时 $m=2$，
\[
J(w,b)=\frac14\left[(w+b-2)^2+(2w+b-3)^2\right].
\]
由上面的公式，
\[
\frac{\partial J}{\partial w}
=\frac12\left[(w+b-2)\cdot1+(2w+b-3)\cdot2\right],
\]
\[
\frac{\partial J}{\partial b}
=\frac12\left[(w+b-2)+(2w+b-3)\right].
\]
代入 $(w,b)=(0,0)$，
\[
\frac{\partial J}{\partial w}(0,0)=\frac12[-2+2(-3)]=-4,\qquad
\frac{\partial J}{\partial b}(0,0)=\frac12(-2-3)=-\frac52.
\]
故
\[
\nabla J(0,0)=\left(-4,-\frac52\right).
\]
若学习率为 $\eta$，第一次更新为
\[
(w_1,b_1)=\left(0,0\right)-\eta\left(-4,-\frac52\right)
=\left(4\eta,\frac52\eta\right).
\]
\end{solution}
"""


convex_ml_block = r"""
\subsection{凸性与机器学习优化}

凸性在优化问题中非常重要. 直观地说，凸函数的图像没有“局部低谷冒充全局最低点”的现象. 在一元情形下，若 $f''(x)\ge0$，则 $f$ 为下凸函数；若严格凸且存在临界点，那么该临界点就是全局最小点. 许多基础机器学习模型，例如线性回归的均方误差损失，关于参数是凸函数，因此可以用导数和梯度方法稳定地寻找最优参数.

\begin{example}
设单样本线性模型损失为
\[
L(w)=\frac12(wx-y)^2,
\]
其中 $x,y$ 为常数. 讨论 $L$ 关于 $w$ 的凸性.
\end{example}
\begin{solution}
对 $w$ 求导：
\[
L'(w)=x(wx-y),\qquad L''(w)=x^2\ge0.
\]
因此 $L$ 关于 $w$ 是下凸函数. 若 $x\neq0$，则 $L''(w)=x^2>0$，函数严格凸，唯一最小点由 $L'(w)=0$ 给出，即
\[
w=\frac{y}{x}.
\]
若 $x=0$，则 $L(w)=\frac12y^2$ 为常数函数，任意 $w$ 都是最小点.
\end{solution}
"""


deriv_body = deriv_body.replace(
    r"\subsection{导数的几何意义与经济意义}",
    gradient_block + "\n" + r"\subsection{导数的几何意义与经济意义}",
    1,
)

mv_start = deriv_body.index(r"\section{微分与多元函数微分}")
mv_end = deriv_body.index(r"\section{中值定理与洛必达法则}", mv_start)
mv_part = deriv_body[mv_start:mv_end]
mv_part = mv_part.replace(
    r"\subsection{课后习题}", multi_ml_block + "\n" + r"\subsection{课后习题}", 1
)
deriv_body = deriv_body[:mv_start] + mv_part + deriv_body[mv_end:]

deriv_body = deriv_body.replace(
    r"\subsection{Taylor 公式}",
    convex_ml_block + "\n" + r"\subsection{Taylor 公式}",
    1,
)


bibliography = r"""
\clearpage
\renewcommand{\refname}{References}
\addcontentsline{toc}{section}{References}
\begin{thebibliography}{99}
\bibitem{JJ} 龚德恩. 经济数学基础：第一分册，微积分. 四川人民出版社. 2016.
\bibitem{TJ} 同济大学数学系. 高等数学. 高等教育出版社.
\bibitem{CJX} 陈纪修，於崇华，金路. 数学分析. 高等教育出版社.
\bibitem{Stewart} Stewart, J. \emph{Calculus: Early Transcendentals}. Cengage Learning.
\bibitem{MacTutorGreek} MacTutor History of Mathematics Archive. Euclid, Archimedes, Apollonius biographies. \url{https://mathshistory.st-andrews.ac.uk/}
\bibitem{MacTutorChinese} MacTutor History of Mathematics Archive. Chinese mathematics overview. \url{https://mathshistory.st-andrews.ac.uk/HistTopics/Chinese_overview/}
\bibitem{MacTutorCalculus} MacTutor History of Mathematics Archive. The rise of calculus. \url{https://mathshistory.st-andrews.ac.uk/HistTopics/The_rise_of_calculus/}
\bibitem{SEP-AI} Stanford Encyclopedia of Philosophy. Artificial Intelligence. \url{https://plato.stanford.edu/entries/artificial-intelligence/}
\bibitem{MathWorldFib} Wolfram MathWorld. Fibonacci Number. \url{https://mathworld.wolfram.com/FibonacciNumber.html}
\end{thebibliography}

\end{document}
"""


OUT.write_text(
    "\n\n".join(
        [
            preamble.strip(),
            history_section.strip(),
            first_body,
            continuity_section.strip(),
            deriv_body,
            bibliography.strip(),
        ]
    )
    + "\n",
    encoding="utf-8",
)

print(f"Wrote {OUT}")
