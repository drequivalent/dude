Dude
==========================================================================

A quick and dirty bash script (for now) that may help the user to find out
where is the free space gone.

Быстрый и грязный скрипт на языке bash (пока что), который поможет понять,
куда девается свободное место.

==========================================================================

Механизм таков: вы создаете два файла с выводом du с некоторым временным
промежутком, к примеру:

du -m /usr > wtfspace1 && sleep 600 && du -m /usr > wtfspace2

А потом, при помощи этого скрипта проверяете, какую директорию раздуло,
и насколько:

dude.sh wtfdiffspace1 wtfdiffspace2 

Можно еще и отсортировать, дабы выявить самых прожорливых:

dude.sh wtfdiffspace1 wtfdiffspace2 | sort -n

За качество кода не бейте, Баш - не моя специализация, и писалось оно
на корую руку. Позже, возможно, перепишу на питоне, а пока - вот так.
