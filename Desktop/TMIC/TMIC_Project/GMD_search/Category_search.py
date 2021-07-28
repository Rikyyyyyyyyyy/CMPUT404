import numpy as np
from compound_class import Compound



def read_code(cp):
    try:
        matrixs = cp.spectrum
        matrixs = matrixs.split(" ")
        matrix = []
        for l in matrixs:
            if l != "":
                m = l.split(":")
                int_map = map(int, m)
                int_list = list(int_map)
                matrix.append(int_list)

        matrix = np.array(matrix)
        matrix = matrix[np.argsort(matrix[:, 1])]
        intensity_list = {}
        for i in matrix:
            intensity_list[i[0]] = i[1]
        script_file = open('data/Scripts.txt', 'r')
        lines = script_file.read().splitlines()

        # we have 3 cases in this file
        # CASE1 single statement
            ## ==
            ## <
            ## >
        # CASE2 or statement
        # CASE3 and statement
        name = lines[0]
        is_compound = True
        for l in lines[1:-1]:
            l = l.lower()
            splited_l = l.split("=", 1)
            try:
                splited_func = splited_l[1].split(" ")
                splited_func = splited_func[1:]
                if len(splited_func) >2:
                    if "and" in splited_func:
                        splited_func.remove("and")
                        for func in splited_func:
                            func_list = func.split("(")
                            if "rank" in func_list[0]:
                                rank_num = int(func_list[1].split(")")[0])
                                compare_num = int(func_list[1].split("=")[1])
                                if matrix[-rank_num][0] == compare_num:
                                    pass
                                else:
                                    is_compound = False
                            if "abundance" in func_list[0]:
                                if "<" in func_list[1]:
                                    abundance_num = int(func_list[1].split(")")[0])
                                    compare_num = int(func_list[1].split("<")[1])
                                    if intensity_list[abundance_num] < compare_num:
                                        pass
                                    else:
                                        is_compound = False
                                elif ">" in func_list[1]:
                                    abundance_num = int(func_list[1].split(")")[0])
                                    compare_num = int(func_list[1].split(">")[1])
                                    if intensity_list[abundance_num] > compare_num:
                                        pass
                                    else:
                                        is_compound = False

                    elif "or" in splited_func:
                        splited_func.remove("or")
                        result_list = []
                        for k in splited_func:
                            func_list = k.split("(")
                            if "rank" in func_list[0]:
                                rank_num = int(func_list[1].split(")")[0])
                                compare_num = int(func_list[1].split("=")[1])
                                if matrix[-rank_num][0] == compare_num:
                                    result_list.append("T")
                                else:
                                    result_list.append("F")

                            if "abundance" in func_list[0]:
                                if "<" in func_list[1]:
                                    abundance_num = int(func_list[1].split(")")[0])
                                    compare_num = int(func_list[1].split("<")[1])
                                    if intensity_list[abundance_num] < compare_num:
                                        result_list.append("T")
                                    else:
                                        result_list.append("F")
                                elif ">" in func_list[1]:
                                    abundance_num = int(func_list[1].split(")")[0])
                                    compare_num = int(func_list[1].split(">")[1])
                                    if intensity_list[abundance_num] > compare_num:
                                        result_list.append("T")
                                    else:
                                        result_list.append("F")
                        if "T" in result_list:
                            pass
                        else:
                            is_compound = False
                else:
                    func_list = splited_func[0].split("(")
                    if "rank" in func_list[0]:
                        rank_num = int(func_list[1].split(")")[0])
                        compare_num = int(func_list[1].split("=")[1])
                        if matrix[-rank_num][0] == compare_num:
                            pass
                        else:
                            is_compound = False
                    if "abundance" in func_list[0]:
                        if "<" in func_list[1]:
                            abundance_num = int(func_list[1].split(")")[0])
                            compare_num = int(func_list[1].split("<")[1])
                            if intensity_list[abundance_num] < compare_num:
                                pass
                            else:
                                is_compound = False
                        elif ">" in func_list[1]:
                            abundance_num = int(func_list[1].split(")")[0])
                            compare_num = int(func_list[1].split(">")[1])
                            if intensity_list[abundance_num] > compare_num:
                                pass
                            else:
                                is_compound = False
            except:
                print("ERROR")
        if is_compound == True:
            cp.set_category(name)

        # if matrix[-1][0] == float(74):
        #     if matrix[-2][0] == float(87) or matrix[-3][0] == float(87):
        #         if intensity_list[55] >150 and intensity_list[55] < 400:
        #             if intensity_list[57] < 350 and intensity_list[59] > 50:
        #                 return "Saturated Fame"
    except:
        print("error")
        return "Unknown"
    return "Unknown"

def category_search(cp):
    str = read_code(cp)
    return str

category_search(cp=Compound(400, "Pentadecanoic acid, methyl ester", "2285 , 1.640", "2265", "1.64", "7132-64-1" , 10,100,100,10,10,10,"74:998 87:546 43:302 41:300 55:281 75:161 59:142 69:108 57:100 143:81 42:62 101:58 83:54 88:44 56:37 97:35 67:35 71:30 157:29 129:29 213:27 53:21 84:21 81:19 171:16 70:15 98:15 256:15 54:15 115:15 73:15 45:14 199:13 95:11 85:11 111:11 185:11 144:10 44:10 79:8 82:8 225:7 76:7 130:7 40:7 68:6 51:5 227:5 109:4 158:4 99:4 65:4 116:4 58:4 112:4 77:3 102:3 125:3 96:3 93:3 214:3 60:3 172:3 107:3 72:2 123:2 113:2 121:1 474:1 228:1 135:1 580:1 91:1 768:1 182:1 165:1 772:1 110:1 139:1 124:1 229:1 100:1 521:1 364:1 342:1 52:1 340:1 86:1 770:1 769:1 94:1 733:1 164:1 773:1 734:1 173:1 579:1 473:1 475:1 731:1 339:1 520:1 771:1 126:1 230:1 506:1 363:1 63:1 137:1 581:0 341:0 252:0 186:0 105:0 257:0 582:0 447:0 61:0 735:0 476:0 537:0 751:0 774:0 250:0 535:0 66:0 578:0 597:0 343:0 365:0 131:0 477:0 251:0 153:0 241:0 163:0 710:0 154:0 403:0 80:0 145:0 183:0 608:0 791:0 104:0 191:0 263:0 562:0 790:0 405:0 577:0 114:0 377:0 305:0 138:0 155:0 641:0 644:0 215:0 62:0 406:0 736:0 281:0 533:0 231:0 564:0 376:0 462:0 749:0 472:0 449:0 505:0 434:0 646:0 502:0 583:0 261:0 563:0 459:0 534:0 549:0 508:0 501:0 684:0 552:0 642:0 478:0 750:0 132:0 460:0 732:0 316:0 362:0 181:0 639:0 195:0 491:0 436:0 792:0 793:0 623:0 553:0 464:0 264:0 517:0 492:0 625:0 775:0 789:0 660:0 259:0 730:0 624:0 551:0 463:0 152:0 753:0 404:0 507:0 754:0 788:0 654:0 656:0 338:0 759:0 262:0 417:0 643:0 668:0 465:0 665:0 547:0 757:0 435:0 767:0 500:0 488:0 366:0 450:0 458:0 672:0 687:0 655:0 304:0 317:0 489:0 548:0 289:0 667:0 255:0 236:0 212:0 196:0 208:0 233:0 290:0 90:0 142:0 48:0 194:0 254:0 136:0 207:0 303:0 159:0 188:0 49:0 50:0 238:0 47:0 147:0 242:0 265:0 313:0 291:0 234:0 211:0 226:0 237:0 178:0 320:0 321:0 64:0 253:0 206:0 325:0 89:0 232:0 306:0 177:0 235:0 331:0 239:0 240:0 146:0 335:0 336:0 337:0 148:0 328:0 46:0 318:0 319:0 106:0 249:0 156:0 134:0 300:0 348:0 349:0 160:0 161:0 210:0 258:0 117:0 332:0 333:0 334:0 170:0 312:0 360:0 314:0 224:0 271:0 151:0 175:0 176:0 367:0 368:0 346:0 133:0 324:0 277:0 326:0 279:0 375:0 329:0 282:0 378:0 189:0 190:0 381:0 192:0 193:0 384:0 385:0 386:0 103:0 293:0 247:0 295:0 296:0 297:0 298:0 204:0 205:0 396:0 397:0 398:0 209:0 400:0 401:0 118:0 119:0 309:0 310:0 216:0 407:0 218:0 219:0 220:0 174:0 222:0 223:0 414:0 415:0 416:0 322:0 323:0 419:0 420:0 421:0 422:0 423:0 424:0 425:0 426:0 427:0 428:0 429:0 430:0 431:0 432:0 433:0 149:0 150:0 246:0 437:0 248:0 439:0 440:0 441:0 442:0 443:0 444:0 445:0 446:0 162:0 448:0 402:0 308:0 166:0 357:0 358:0 359:0 455:0 456:0 267:0 268:0 269:0 270:0 461:0 272:0 273:0 179:0 180:0 466:0 467:0 278:0 469:0 470:0 471:0 92:0 283:0 284:0 380:0 286:0 382:0 383:0 479:0 480:0 481:0 482:0 483:0 294:0 485:0 486:0 487:0 108:0 299:0 490:0 301:0 302:0 493:0 399:0 495:0 496:0 260:0 498:0 499:0 120:0 311:0 122:0 503:0 504:0 315:0 221:0 127:0 128:0 509:0 510:0 511:0 512:0 513:0 514:0 515:0 516:0 327:0 518:0 519:0 140:0 141:0 522:0 523:0 524:0 525:0 526:0 527:0 528:0 529:0 530:0 531:0 532:0 438:0 344:0 345:0 536:0 347:0 538:0 539:0 540:0 541:0 542:0 543:0 497:0 545:0 546:0 167:0 168:0 169:0 550:0 361:0 457:0 78:0 554:0 555:0 556:0 557:0 558:0 559:0 560:0 561:0 372:0 468:0 184:0 565:0 566:0 187:0 568:0 569:0 570:0 571:0 572:0 573:0 574:0 575:0 576:0 197:0 198:0 484:0 200:0 201:0 202:0 203:0 584:0 585:0 586:0 587:0 588:0 589:0 590:0 591:0 592:0 593:0 594:0 595:0 596:0 217:0 598:0 599:0 600:0 601:0 602:0 603:0 604:0 605:0 606:0 607:0 418:0 609:0 610:0 611:0 612:0 613:0 614:0 615:0 616:0 617:0 618:0 619:0 620:0 621:0 622:0 243:0 244:0 245:0 626:0 627:0 628:0 629:0 630:0 631:0 632:0 633:0 634:0 635:0 636:0 637:0 638:0 544:0 640:0 451:0 452:0 453:0 454:0 645:0 266:0 647:0 648:0 649:0 650:0 651:0 652:0 653:0 274:0 275:0 276:0 657:0 658:0 659:0 280:0 661:0 662:0 663:0 664:0 285:0 666:0 287:0 288:0 669:0 670:0 671:0 292:0 673:0 674:0 675:0 676:0 677:0 678:0 679:0 680:0 681:0 682:0 683:0 494:0 685:0 686:0 307:0 688:0 689:0 690:0 691:0 692:0 693:0 694:0 695:0 696:0 697:0 698:0 699:0 700:0 701:0 702:0 703:0 704:0 705:0 706:0 707:0 708:0 709:0 330:0 711:0 712:0 713:0 714:0 715:0 716:0 717:0 718:0 719:0 720:0 721:0 722:0 723:0 724:0 725:0 726:0 727:0 728:0 729:0 350:0 351:0 352:0 353:0 354:0 355:0 356:0 737:0 738:0 739:0 740:0 741:0 742:0 743:0 744:0 745:0 746:0 747:0 748:0 369:0 370:0 371:0 752:0 373:0 374:0 755:0 756:0 567:0 758:0 379:0 760:0 761:0 762:0 763:0 764:0 765:0 766:0 387:0 388:0 389:0 390:0 391:0 392:0 393:0 394:0 395:0 776:0 777:0 778:0 779:0 780:0 781:0 782:0 783:0 784:0 785:0 786:0 787:0 408:0 409:0 410:0 411:0 412:0 413:0 794:0 795:0 796:0 797:0 798:0 799:0 800:0"))

