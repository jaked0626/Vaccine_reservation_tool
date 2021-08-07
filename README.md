# Vaccine_reservation_tool
大手町の自衛隊大規模接種会場でのワクチン予約の流れを自動化するプログラム.

selenium をつかって自動的にウェブページを随時更新し、空きを確認しては予約をおさえます。
使い方:
1. Python をインストールする（Anaconda　というdistribution がおすすめ)
2. コマンドラインから、selenium と webdriver_managerをインストールする　(run the code: 'pip install selenium webdriver_manager' on command line)
3. Google Chrome もなければインストールする
4. python3 reserve_vaccine.py と打つ
5. 指示通り、必要情報を記入する　

注：はじめて起動する際は、一度手動でワクチン予約ホームページにログインし、カレンダーページまで進んでからご利用ください。さもなくばエラーでプログラムがexitします。  

注：reserve_vaccine.pyは再編集後，予約までのテストを行えていないので，エラーがあるようでしたら, backups/new_vaccines.py をお使いください．
