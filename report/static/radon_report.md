# Radon Report
---
## Cyclomatic Complexity
| File | Type | Name | Complexity | Rank |
| --- | --- | --- | --- | --- |
| src\Application.py | F | main | 2 | A |
| src\Configurator.py | C | MainWindow | 4 | A |
| src\Configurator.py | M | __init__ | 1 | A |
| src\Configurator.py | M | update_right_list | 4 | A |
| src\Configurator.py | M | update_labels_and_text_boxes | 4 | A |
| src\Generator.py | F | getLoggingLevel | 1 | A |
| src\Generator.py | F | generateConfig | 3 | A |
| src\Generator.py | F | writeConfig | 5 | A |
| src\Generator.py | F | unnestDict | 3 | A |
| src\Generator.py | F | loadDTC | 2 | A |
| src\Generator.py | F | generateDTC | 3 | A |
| src\Generator.py | F | loadConfig | 1 | A |
| src\Generator.py | F | main | 1 | A |
| src\pyDiagnostic\diagnostic.py | C | Inspector | 3 | A |
| src\pyDiagnostic\diagnostic.py | M | __new__ | 4 | A |
| src\pyDiagnostic\diagnostic.py | M | __init__ | 3 | A |
| src\pyDiagnostic\diagnostic.py | M | _setup_stream_handler | 1 | A |
| src\pyDiagnostic\diagnostic.py | M | _setup_file_handler | 1 | A |
| src\pyDiagnostic\diagnostic.py | M | clear_DTC | 1 | A |
| src\pyDiagnostic\diagnostic.py | M | clean_up | 3 | A |
| src\pyDiagnostic\diagnostic.py | M | set_event_status | 3 | A |
| src\pyDiagnostic\diagnostic.py | M | look_up | 2 | A |
| src\pyDiagnostic\diagnostic.py | M | dump_DTC | 3 | A |
| src\pyDiagnostic\diagnostic.py | M | last_event | 2 | A |
| src\pyDiagnostic\__sample.py | F | DDX_normal_usecase | 4 | A |
| src\pyDummy\dummy.py | C | clsDummy | 2 | A |
| src\pyDummy\dummy.py | M | __init__ | 1 | A |
| src\pyDummy\dummy.py | M | foo | 2 | A |
| src\pyDummy\dummy.py | M | baz | 1 | A |
| src\pyFileManagement\fileManage.py | F | walk_tree | 1 | A |
| src\pyPkmHome\image_process.py | F | extractText | 11 | C |
| src\pyPkmHome\image_process.py | F | extractColorHex | 3 | A |
| src\pyPkmHome\image_process.py | F | searchImage | 14 | C |
| src\pyPkmHome\pokemon_HOME.py | F | extractNatureStats | 6 | B |
| src\pyPkmHome\pokemon_HOME.py | F | extractStatsIV | 3 | A |
| src\pyPkmHome\pokemon_HOME.py | F | extractMain | 3 | A |
| src\pyPkmHome\pokemon_HOME.py | F | extractGender | 3 | A |
| src\pyPkmHome\pokemon_HOME.py | F | mainFunction | 5 | A |
| src\pyPkmHome\_generateCode.py | F | createRetangleDict | 5 | A |
| src\pyPkmHome\_generateCode.py | F | extractDict | 3 | A |
| src\pyPkmHome\_generateCode.py | F | mainFunction | 1 | A |
| src\pyTorrent\torrent_1337x.py | F | convert_size | 3 | A |
| src\pyTorrent\torrent_1337x.py | C | TorrentSearch | 6 | B |
| src\pyTorrent\torrent_1337x.py | M | __init__ | 3 | A |
| src\pyTorrent\torrent_1337x.py | M | __setattr__ | 7 | B |
| src\pyTorrent\torrent_1337x.py | M | get_magnet_link | 2 | A |
| src\pyTorrent\torrent_1337x.py | M | get_torrent_links | 10 | B |
| src\pyUpdate\Update.py | C | GitHubRepo | 3 | A |
| src\pyUpdate\Update.py | M | __init__ | 4 | A |
| src\pyUpdate\Update.py | M | get_latest_version | 2 | A |
| src\pyUpdate\Update.py | M | pull_latest_version | 2 | A |
| src\pyUpdate\Update.py | M | restart_application | 2 | A |
| src\pyUpdate\Update.py | M | update_application | 3 | A |
| src\pyUpdate\Update.py | M | get_current_version | 2 | A |

## Other Metrics
| File | LOC | LLOC | SLOC | Comments | Multi | Blank | H1 | H2 | N1 | N2 | Vocabulary | Length | Calculated Length | Volume | Difficulty | Effort | MI |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| src\Application.py | 38 | 17 | 22 | 4 | 3 | 9 | 1 | 4 | 2 | 4 | 5 | 6 | 8.0 | 13.932 | 0.5 | 6.966 | 91.654 |
| src\Configurator.py | 77 | 59 | 59 | 3 | 0 | 15 | 1 | 6 | 4 | 8 | 7 | 12 | 15.51 | 33.688 | 0.667 | 22.459 | 62.501 |
| src\Generator.py | 184 | 73 | 79 | 10 | 55 | 40 | 7 | 19 | 12 | 21 | 26 | 33 | 100.362 | 155.115 | 3.868 | 600.048 | 70.123 |
| src\Scheduler.py | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 |
| src\_CONST_.py | 10 | 14 | 7 | 2 | 0 | 1 | 1 | 1 | 1 | 1 | 2 | 2 | 0.0 | 2.0 | 0.5 | 1.0 | 98.914 |
| src\__init__.py | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 |
| src\pyAbstract\CALLBACK.py | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 |
| src\pyDiagnostic\diagnostic.py | 162 | 77 | 79 | 3 | 46 | 32 | 3 | 12 | 7 | 12 | 15 | 19 | 47.774 | 74.231 | 1.5 | 111.346 | 71.707 |
| src\pyDiagnostic\_CONST_.py | 18 | 19 | 10 | 4 | 0 | 4 | 1 | 1 | 1 | 1 | 2 | 2 | 0.0 | 2.0 | 0.5 | 1.0 | 98.118 |
| src\pyDiagnostic\__init__.py | 33 | 2 | 1 | 28 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 |
| src\pyDiagnostic\__sample.py | 33 | 12 | 18 | 6 | 0 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 |
| src\pyDummy\dummy.py | 11 | 10 | 9 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 |
| src\pyFileManagement\fileManage.py | 5 | 3 | 3 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 |
| src\pyFileManagement\__init__.py | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 |
| src\pyFileManagement\__literals__.py | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 |
| src\pyPkmHome\image_process.py | 186 | 59 | 95 | 24 | 23 | 44 | 11 | 62 | 34 | 67 | 73 | 101 | 407.214 | 625.172 | 5.944 | 3715.742 | 67.348 |
| src\pyPkmHome\pokemon_HOME.py | 201 | 66 | 93 | 38 | 30 | 44 | 3 | 20 | 12 | 23 | 23 | 35 | 91.193 | 158.325 | 1.725 | 273.11 | 71.406 |
| src\pyPkmHome\_CONST_.py | 102 | 43 | 76 | 50 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 |
| src\pyPkmHome\_generateCode.py | 87 | 34 | 41 | 8 | 20 | 18 | 3 | 6 | 4 | 7 | 9 | 11 | 20.265 | 34.869 | 1.75 | 61.021 | 83.798 |
| src\pyPkmHome\__init__.py | 12 | 2 | 1 | 3 | 5 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 |
| src\pySocket\echo-client.py | 11 | 8 | 8 | 2 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 |
| src\pyTorrent\torrent_1337x.py | 184 | 60 | 95 | 2 | 53 | 34 | 10 | 42 | 25 | 48 | 52 | 73 | 259.697 | 416.132 | 5.714 | 2377.898 | 68.748 |
| src\pyTorrent\_CONST_.py | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 |
| src\pyTorrent\__init__.py | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 |
| src\pyTorrent\__sample.py | 47 | 19 | 28 | 8 | 0 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 |
| src\pyUpdate\Update.py | 123 | 55 | 53 | 0 | 36 | 34 | 3 | 12 | 7 | 12 | 15 | 19 | 47.774 | 74.231 | 1.5 | 111.346 | 75.752 |
| src\pyUpdate\__init__.py | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 |
| src\pyUpdate\__sample.py | 7 | 3 | 3 | 2 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 |

