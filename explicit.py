import logging
import re

logger = logging.getLogger(f'TrueModer.{__name__}')

my_patterns = (
    r'^(\w*бля\w*)$',
    r'([нпз]?[?аео]?[хк]у[йеё]\w*)',
    r'\w*п[иi]зд\w*'

)

external_patterns = (
    # основной фильтр
    # '(?:\w*(?:[хxh](?:[уyu][иiu])|[пnp][еиeiu](?:[з3z][дd]|[дd](?:[еаоeoa0][рpr]|[рpr]))|[бb6][лl]я[дd]|[оo0][хxh][уyu]'
    # '[еe]|[мm][уyu][дd][еоиаeioau0]|[дd][еe][рpr][ьb]|[гrg][аоoa0][вbv][нhn]|[уyu][еёe][бb6])|[хxh][\W_]*(?:[уyu][\W_]*'
    # '[йиеёяeiju])|[пnp][\W_]*[еиeiu][\W_]*(?:[з3z][\W_]*[дd]|[дd][\W_]*(?:[еаоeoa0][\W_]*[рpr]|[рpr]))|[бb6][\W_]*[лl]'
    # '[\W_]*я[\W_]*[дd]|[оo0][\W_]*[хxh][\W_]*[уyu][\W_]*[еe]|[мm][\W_]*[уyu][\W_]*[дd][\W_]*[еоиаeioau0]|[дd][\W_]*[еe]'
    # '[\W_]*[рpr][\W_]*[ьb]|[гrg][\W_]*[аоoa0][\W_]*[вbv][\W_]*[нhn]|[уyu][\W_]*[еёe][\W_]*[бb6]|[ёеe][бb6])\w+',

    # жоп*
    'ж[\W_]*(?:[оo0][\W_]*[пnp][\W_]*(?:[аa]|[oо0](?:[\W_]*[хxh])?|[уеыeyiuё]|[оo0][\W_]*[йj])\w*)',

    # дерьмо
    '[дd][\W_]*[еe][\W_]*[рpr][\W_]*(?:[ьb][\W_]*)?[мm][\W_]*[оуеаeoya0u](?:[\W_]*[мm])?',

    # чмо, чмырь
    '[чc][\W_]*[мm][\W_]*(?:[оo0]|[ыi][\W_]*[рpr][\W_]*[еиьяeibu])',

    # сука, сучка
    '[сsc][\W_]*[уuy][\W_]*(?:(?:[чc][\W_]*)?[кk][\W_]*[ауиiyau](?:[\W_]*[нhn](?:[\W_]*[оo0][\W_]*[йj]|[\W_]*[уаыyiau])'
    '?)?|[чc][\W_]*(?:(?:[ьb][\W_]*)?(?:[еёяиeiu]|[еиeiu][\W_]*[йj])|[аa][\W_]*[рpr][\W_]*[ыауеeyiau]))',

    # гондон
    '[гrg][\W_]*(?:[аоoa0][\W_]*(?:[нhn][\W_]*[дd][\W_]*[аоoa0][\W_]*[нhn](?:[\W_]*[ыуyiu])?|[вbv][\W_]*[нhn][\W_]*'
    '[оаoa0](?:[\W_]*(?:[мm]|[еe][\W_]*[дd](?:[\W_]*[ыуаеeyiau]|[\W_]*[оаoa0][\W_]*[мm](?:[\W_]*[иiu])?)?))?)|[нhn]'
    '[\W_]*(?:[иiu][\W_]*[дd][\W_]*(?:[ыуеаeyiau]|[оo0][\W_]*[йj])|[уyu][сsc](?:[\W_]*[аыуyiau]|[\W_]*[оаoa0][\W_]*'
    '[мm](?:[\W_]*[иiu])?)?))',

    # *еб*
    '(?:[нhn][\W_]*[еe][\W_]*)?(?:(?:[з3z][\W_]*[аa]|[оo0][тt]|[пnp][\W_]*[оo0]|[пnp][\W_]*(?:[еe][\W_]*[рpr][\W_]*[еe]|[рpr][\W_]*[оеиeiou0]|[иiu][\W_]*[з3z][\W_]*[дd][\W_]*[оo0])|[нhn][\W_]*[аa]|[иiu][\W_]*[з3z]|[дd][\W_]*[оo0]|[вbv][\W_]*[ыi]|[уyu]|[рpr][\W_]*[аa][\W_]*[з3z]|[з3z][\W_]*[лl][\W_]*[оo0]|[тt][\W_]*[рpr][\W_]*[оo0]|[уyu])[\W_]*)?(?:[вbv][\W_]*[ыi][\W_]*)?(?:[ъьb][\W_]*)?(?:[еёe][\W_]*[бb6](?:(?:[\W_]*[оеёаиуeioyau0])?(?:[\W_]*[нhn](?:[\W_]*[нhn])?[\W_]*[яуаиьiybau]?)?(?:[\W_]*[вbv][\W_]*[аa])?(?:(?:[\W_]*(?:[иеeiu]ш[\W_]*[ьb][\W_]*[сsc][\W_]*я|[тt][\W_]*(?:(?:[ьb][\W_]*)?[сsc][\W_]*я|[ьb]|[еe][\W_]*[сsc][\W_]*[ьb]|[еe]|[оo0]|[иiu][\W_]*[нhn][\W_]*[уыеаeyiau])|(?:щ[\W_]*(?:[иiu][\W_]*[йj]|[аa][\W_]*я|[иеeiu][\W_]*[еe]|[еe][\W_]*[гrg][\W_]*[оo0])|ю[\W_]*[тt])(?:[\W_]*[сsc][\W_]*я)?|[еe][\W_]*[мтmt]|[кk](?:[\W_]*[иаiau])?|[аa][\W_]*[лl](?:[\W_]*[сsc][\W_]*я)?|[лl][\W_]*(?:[аa][\W_]*[нhn]|[оаoa0](?:[\W_]*[мm])?|(?:[иiu][\W_]*)?[сsc][\W_]*[ьяb]|[иiu]|[аa][\W_]*[сsc][\W_]*[ьb])|[рpr][\W_]*[ьb]|[сsc][\W_]*[яьb]|[нhn][\W_]*[оo0]|[чc][\W_]*(?:[иiu][\W_]*[хxh]|[еe][\W_]*[сsc][\W_]*[тt][\W_]*[ьиibu](?:[\W_]*ю)?)|(?:[тt][\W_]*[еe][\W_]*[лl][\W_]*[ьb][\W_]*[сsc][\W_]*[кk][\W_]*|[сsc][\W_]*[тt][\W_]*|[лl][\W_]*[иiu][\W_]*[вbv][\W_]*|[чтtc][\W_]*)?(?:[аa][\W_]*я|[оo0][\W_]*[йемejm]|[ыi][\W_]*[хйеejxh]|[ыi][\W_]*[мm](?:[\W_]*[иiu])?|[уyu][\W_]*ю|[иiu][\W_]*[еe]|[оo0][\W_]*[мm][\W_]*[уyu]|[иiu][\W_]*[йj]|[еe][\W_]*[вbv]|[иiu][\W_]*[мm](?:[\W_]*[иiu])?)|[чтыйилijltcu]))?)|[\W_]*[ыi](?:(?:[\W_]*[вbv][\W_]*[аa]|[\W_]*[нhn](?:[\W_]*[нhn])?)(?:(?:[\W_]*(?:[иеeiu]ш[\W_]*[ьb][\W_]*[сsc][\W_]*я|[тt][\W_]*(?:[ьb][\W_]*[сsc][\W_]*я|[ьb]|[еe][\W_]*[сsc][\W_]*[ьb]|[еe]|[иiu][\W_]*[нhn][\W_]*[уыеаeyiau])|(?:щ[\W_]*(?:[иiu][\W_]*[йj]|[аa][\W_]*я|[иеeiu][\W_]*[еe]|[еe][\W_]*[гrg][\W_]*[оo0])|ю[\W_]*[тt])(?:[\W_]*[сsc][\W_]*я)?|[еe][\W_]*[мтmt]|[лl][\W_]*(?:(?:[иiu][\W_]*)?[сsc][\W_]*[ьяb]|[иiu]|[аa][\W_]*[сsc][\W_]*[ьb])|(?:[сsc][\W_]*[тt][\W_]*|[лl][\W_]*[иiu][\W_]*[вbv][\W_]*|[чтtc][\W_]*)?(?:[аa][\W_]*я|[оo0][\W_]*[йемejm]|[ыi][\W_]*[хйеejxh]|[ыi][\W_]*[мm](?:[\W_]*[иiu])?|[уyu][\W_]*ю|[иiu][\W_]*[еe]|[оo0][\W_]*[мm][\W_]*[уyu]|[иiu][\W_]*[йj]|[еe][\W_]*[вbv]|[иiu][\W_]*[мm](?:[\W_]*[иiu])?))))|[рpr][\W_]*[ьb]))|я[\W_]*[бb6](?:[\W_]*[оеёаиуeioyau0])?(?:(?:[\W_]*[нhn](?:[\W_]*[нhn])?[\W_]*[яуаиьiybau]?)?(?:(?:[\W_]*(?:[иеeiu]ш[\W_]*[ьb][\W_]*[сsc][\W_]*я|[тt][\W_]*(?:[ьb][\W_]*[сsc][\W_]*я|[ьb]|[еe][\W_]*[сsc][\W_]*[ьb]|[еe]|[иiu][\W_]*[нhn][\W_]*[уыеаeyiau])|(?:щ[\W_]*(?:[иiu][\W_]*[йj]|[аa][\W_]*я|[иеeiu][\W_]*[еe]|[еe][\W_]*[гrg][\W_]*[оo0])|ю[\W_]*[тt])(?:[\W_]*[сsc][\W_]*я)?|[еe][\W_]*[мтmt]|[кk](?:[\W_]*[иаiau])?|[аa][\W_]*[лl](?:[\W_]*[сsc][\W_]*я)?|[лl][\W_]*(?:[аa][\W_]*[нhn]|[оаoa0](?:[\W_]*[мm])?|(?:[иiu][\W_]*)?[сsc][\W_]*[ьяb]|[иiu])|[рpr][\W_]*[ьb]|[сsc][\W_]*[яьb]|[нhn][\W_]*[оo0]|[чc][\W_]*(?:[иiu][\W_]*[хxh]|[еe][\W_]*[сsc][\W_]*[тt][\W_]*[ьиibu](?:[\W_]*ю)?)|(?:[тt][\W_]*[еe][\W_]*[лl][\W_]*[ьb][\W_]*[сsc][\W_]*[кk][\W_]*|[сsc][\W_]*[тt][\W_]*|[лl][\W_]*[иiu][\W_]*[вbv][\W_]*|[чтtc][\W_]*)?(?:[аa][\W_]*я|[оo0][\W_]*[йемejm]|[ыi][\W_]*[хйеejxh]|[ыi][\W_]*[мm](?:[\W_]*[иiu])?|[уyu][\W_]*ю|[иiu][\W_]*[еe]|[оo0][\W_]*[мm][\W_]*[уyu]|[иiu][\W_]*[йj]|[еe][\W_]*[вbv]|[иiu][\W_]*[мm](?:[\W_]*[иiu])?)|[чмйилijlmcu]))|(?:[\W_]*[нhn](?:[\W_]*[нhn])?[\W_]*[яуаиьiybau]?)))|я[\W_]*[бb6][\W_]*(?:[еёаиуeiyau][\W_]*)?(?:[нhn][\W_]*(?:[нhn][\W_]*)?(?:[яуаиьiybau][\W_]*)?)?[тt])'

    # *выебан*
    '\w*[вbv][\W_]*([ыиiu]+[\W_]*[еёe]+[\W_]*[бb6][\W_]*[аоoa0][\W_]*[нhn])\w*',

    # (с,об)ьеб*
    '([сsc]|[оo0][\W_]*[бb6])[\W_]*[ьъb][\W_]*[еяёe][\W_]*[бb6][\W_]*(?:([уyu]|[оo0][\W_]*[сз3szc])|(?:[еиёауeiyau](?:[\W_]*[лl](?:[\W_]*[иоаioau0])?|[\W_]*ш[\W_]*[ьb]|[\W_]*[тt][\W_]*[еe])?(?:[\W_]*[сsc][\W_]*[ьяb])?))',

    # еб*
    '[еe][\W_]*(?:[бb6][\W_]*(?:[уyu][\W_]*[кk][\W_]*[еe][\W_]*[нhn][\W_]*[тt][\W_]*[иiu][\W_]*[йj]|[еe][\W_]*[нhn][\W_]*(?:[ьb]|я(?:[\W_]*[мm])?)|[иiu][\W_]*(?:[цc][\W_]*[кk][\W_]*[аa][\W_]*я|[чc][\W_]*[еe][\W_]*[сsc][\W_]*[кk][\W_]*[аa][\W_]*я)|[лl][\W_]*[иiu][\W_]*щ[\W_]*[еe]|[аa][\W_]*(?:[лl][\W_]*[ьb][\W_]*[нhn][\W_]*[иiu][\W_]*[кk](?:[\W_]*[иаiau])?|[тt][\W_]*[оo0][\W_]*[рpr][\W_]*[иiu][\W_]*[йj]|[нhn][\W_]*(?:[тt][\W_]*[рpr][\W_]*[оo0][\W_]*[пnp]|[аa][\W_]*[тt][\W_]*[иiu][\W_]*(?:[кk]|[чc][\W_]*[еe][\W_]*[сsc][\W_]*[кk][\W_]*[иiu][\W_]*[йj]))))|[дd][\W_]*[рpr][\W_]*[иiu][\W_]*[тt])',

    # невротъебательск*
    '[нhn][\W_]*[еe][\W_]*[вbv][\W_]*[рpr][\W_]*[оo0][\W_]*[тt][\W_]*ъ[\W_]*[еe][\W_]*[бb6][\W_]*[аa][\W_]*[тt][\W_]*[еe][\W_]*[лl][\W_]*[ьb][\W_]*[сsc][\W_]*[кk][\W_]*[иiu][\W_]*(?:[ыиiu][\W_]*[йj]|[аa][\W_]*я|[оo0][\W_]*[ейej]|[ыi][\W_]*[хxh]|[ыi][\W_]*[еe]|[ыi][\W_]*[мm](?:[\W_]*[иiu])?|[уyu][\W_]*ю|[оo0][\W_]*[мm][\W_]*[уyu])',

    # уёбищ*
    '[уyu][\W_]*(?:[ёеe][\W_]*[бb6][\W_]*(?:[иiu][\W_]*щ[\W_]*[еаea]|[аa][\W_]*[нhn](?:[\W_]*[тt][\W_]*[уyu][\W_]*[сsc])?(?:[\W_]*[аоoa0][\W_]*[вмbmv]|[\W_]*[ыуеаeyiau])?)|[рpr][\W_]*[оo0][\W_]*[дd](?:[\W_]*[аоoa0][\W_]*[вмbmv]|[\W_]*[ыуеаeyiau])?|[бb6][\W_]*[лl][\W_]*ю[\W_]*[дd][\W_]*(?:[оo0][\W_]*[кk]|[кk][\W_]*(?:[аоoa0][\W_]*[вмbmv](?:[\W_]*[иiu])?|[иуеаeiyau])?))',

    # муд*
    '[мm][\W_]*(?:[уyu][\W_]*[дd][\W_]*(?:[оo0][\W_]*[хxh][\W_]*[аa][\W_]*(?:[тt][\W_]*[ьb][\W_]*[сsc][\W_]*я|ю[\W_]*[сsc][\W_]*[ьb]|[еe][\W_]*ш[\W_]*[ьb][\W_]*[сsc][\W_]*я)|[аa][\W_]*(?:[кk](?:[\W_]*[иаiau]|[оo0][мвbmv])?|[чc][\W_]*(?:[ьb][\W_]*[еёe]|[иiu][\W_]*[нhn][\W_]*[уыаyiau]|[кk][\W_]*(?:[аиеуeiyau]|[оo0][\W_]*[йj])))|[еe][\W_]*[нhn][\W_]*[ьb]|[иiu][\W_]*[лl](?:[\W_]*[аеоыeoia0]?))|[аa][\W_]*[нhn][\W_]*[дd][\W_]*[уаyau]|[лl][\W_]*(?:[иiu][\W_]*[нhn]|я))',

    # (мозг/долб/скот/...)(хуй|еб)|ство
    '(?:[мm][\W_]*(?:[оo0][\W_]*[з3z][\W_]*[гrg]|[уyu][\W_]*[дd])|[дd][\W_]*(?:[оo0][\W_]*[лl][\W_]*[бb6]|[уyu][\W_]*[рpr])|[сsc][\W_]*[кk][\W_]*[оo0][\W_]*[тt])[\W_]*[аоoa0][\W_]*(?:[хxh][\W_]*[уyu][\W_]*[ийяiju]|[ёеe][\W_]*[бb6](?:[\W_]*[еоeo0][\W_]*[вbv]|[\W_]*[ыаia]|[\W_]*[сsc][\W_]*[тt][\W_]*[вbv][\W_]*[оуoy0u](?:[\W_]*[мm])?|[иiu][\W_]*[з3z][\W_]*[мm])?)',

    # *пизд/еб*
    '(?:[нhn][\W_]*[еe][\W_]*|[з3z][\W_]*[аa][\W_]*|[оo0][\W_]*[тt][\W_]*|[пnp][\W_]*[оo0][\W_]*|[нhn][\W_]*[аa][\W_]*|[рpr][\W_]*[аa][\W_]*[сз3szc][\W_]*)?(?:[пnp][\W_]*[иiu][\W_]*[з3z][\W_]*[дd][\W_]*[ияеeiu]|(?:ъ)?[еёe][\W_]*[бb6][\W_]*[аa])[\W_]*(?:(?:([тt][\W_]*[ьb]|[лl])[\W_]*[сsc][\W_]*я|[тt][\W_]*[ьb]|[лl][\W_]*[иiu]|[аa][\W_]*[лl]|[лl]|c[\W_]*[ьb]|[иiu][\W_]*[тt]|[иiu]|[тt][\W_]*[еe]|[чc][\W_]*[уyu]|ш[\W_]*[ьb])|(?:[йяиiju]|[иеeiu][\W_]*[мm](?:[\W_]*[иiu])?|[йj][\W_]*[сsc][\W_]*(?:[кk][\W_]*(?:[ыиiu][\W_]*[йеej]|[аa][\W_]*я|[оo0][\W_]*[еe]|[ыi][\W_]*[хxh]|[ыi][\W_]*[мm](?:[\W_]*[иiu])?|[уyu][\W_]*ю|[оo0][\W_]*[мm][\W_]*[уyu])|[тt][\W_]*[вbv][\W_]*[оуаoya0u](?:[\W_]*[мm])?)))',

    # пидор*
    '[пnp][\W_]*[еиыeiu][\W_]*[дd][\W_]*[аеэоeoa0][\W_]*[рpr](?:(?:[\W_]*[аa][\W_]*[сз3szc](?:(?:[\W_]*[тt])?(?:[\W_]*[ыi]|[\W_]*[оаoa0][\W_]*[мm](?:[\W_]*[иiu])?|[\W_]*[кk][\W_]*[аиiau])?|(?:[\W_]*[ыуаеeyiau]|[\W_]*[оаoa0][\W_]*[мm](?:[\W_]*[иiu])?|[\W_]*[оo0][\W_]*[вbv])))|[\W_]*(?:[ыуаеeyiau]|[оаoa0][\W_]*[мm](?:[\W_]*[иiu])?|[оo0][\W_]*[вbv]|[нhn][\W_]*я))?',

    # пизд*
    '[пnp][\W_]*[иiu][\W_]*[з3z][\W_]*(?:[ьb][\W_]*)?[дd][\W_]*(?:[ёеe][\W_]*(?:[нhn][\W_]*[ыi][\W_]*ш(?:[\W_]*[ьb])?|'
    '[шнжhn](?:[\W_]*[ьb])?)|[уyu][\W_]*(?:[йj](?:[\W_]*[тt][\W_]*[еe])?|[нhn](?:[\W_]*[ыi])?)|ю[\W_]*(?:[кk](?:[\W_]*'
    '(?:[аеуиeiyau]|[оo0][\W_]*[вbv]|[аa][\W_]*[мm](?:[\W_]*[иiu])?))?|[лl](?:[ьиibu]|[еe][\W_]*[йj]|я[\W_]*[хмmxh]))|'
    '[еe][\W_]*[цc]|[аоoa0][\W_]*(?:[нhn][\W_]*[уyu][\W_]*)?[тt][\W_]*(?:[иiu][\W_]*[йj]|[аa][\W_]*я|[оo0](?:[\W_]*'
    '[ейej])?|[ыi][\W_]*[ейхejxh]|[ыi][\W_]*[мm](?:[\W_]*[иiu])?|[уyu][\W_]*ю|[оo0][\W_]*[мm][\W_]*[уyu]|[еe][\W_]*'
    '[еe]|[ауьеыeyibau])|[аa][\W_]*[нhn][\W_]*[уyu][\W_]*[лl](?:[\W_]*[аиiau])?|[ыеуиаeiyau]|[оаoa0][\W_]*(?:[йj]|'
    '[хxh][\W_]*[уyu][\W_]*[йj]|[еёe][\W_]*[бb6]|(?:[рpr][\W_]*[оo0][\W_]*[тt]|[гrg][\W_]*[оo0][\W_]*[лl][\W_]*[оo0]'
    '[\W_]*[вbv])[\W_]*(?:[ыиiu][\W_]*[йj]|[аa][\W_]*я|[оo0][\W_]*[ейej]|[ыi][\W_]*[хxh]|[ыi][\W_]*[еe]|[ыi][\W_]*[мm]'
    '(?:[\W_]*[иiu])?|[уyu][\W_]*ю|[оo0][\W_]*[мm][\W_]*[уyu])|[бb6][\W_]*(?:[рpr][\W_]*[аa][\W_]*[тt][\W_]*[иiu][\W_]'
    '*я|[оo0][\W_]*[лl](?:[\W_]*[аыуyiau])?)))',

    # падл*
    '[пnp][\W_]*(?:[аa][\W_]*[дd][\W_]*[лl][\W_]*[аоыoia0]|[оаoa0][\W_]*[сsc][\W_]*[кk][\W_]*[уyu][\W_]*[дd][\W_]*(?:[ыуаеeyiau]|[оаoa0][\W_]*[мm](?:[\W_]*[иiu])?)|[иеeiu][\W_]*[дd][\W_]*(?:[иiu][\W_]*[кk]|[рpr][\W_]*[иiu][\W_]*[лl](?:[\W_]*[лl])?)(?:[\W_]*[оаoa0][\W_]*[мвbmv]|[\W_]*[иуеоыаeioyau0])?|[рpr][\W_]*[оo0][\W_]*[бb6][\W_]*[лl][\W_]*я[\W_]*[дd][\W_]*[оo0][\W_]*[мm])',

    # *срать*
    '(?:[з3z][\W_]*[аa][\W_]*|[оo0][\W_]*[тt][\W_]*|[нhn][\W_]*[аa][\W_]*)?[сsc][\W_]*[рpr][\W_]*(?:[аa][\W_]*[тt][\W_]*[ьb]|[аa][\W_]*[лl](?:[\W_]*[иiu])?|[eуиiyu])',

    # срак*
    '[сsc][\W_]*[рpr][\W_]*[аa][\W_]*(?:[кk][\W_]*(?:[аеиуeiyau]|[оo0][\W_]*[йj])|[нhn](?:[\W_]*[нhn])?(?:[ьb]|(?:[\W_]*[ыi][\W_]*[йеej]|[\W_]*[аa][\W_]*я|[\W_]*[оo0][\W_]*[еe]))|[лl][\W_]*[ьb][\W_]*[нhn][\W_]*[иiu][\W_]*[кk](?:[\W_]*[иiu]|[\W_]*[оаoa0][\W_]*[мm])?)',

    # *трах*
    '(?:[з3z][\W_]*[аa][\W_]*)?[тt][\W_]*[рpr][\W_]*[аa][\W_]*[хxh][\W_]*(?:[нhn][\W_]*(?:[уyu](?:[\W_]*[тt][\W_]*[ьb](?:[\W_]*[сsc][\W_]*я)?|[\W_]*[сsc][\W_]*[ьb]|[\W_]*[лl](?:[\W_]*[аиiau])?)?|[еиeiu][\W_]*ш[\W_]*[ьb][\W_]*[сsc][\W_]*я)|[аa][\W_]*(?:[лl](?:[\W_]*[аоиioau0])?|[тt][\W_]*[ьb](?:[\W_]*[сsc][\W_]*я)?|[нhn][\W_]*(?:[нhn][\W_]*)?(?:[ыиiu][\W_]*[йj]|[аa][\W_]*я|[оo0][\W_]*[йеej]|[ыi][\W_]*[хxh]|[ыi][\W_]*[еe]|[ыi][\W_]*[мm](?:[\W_]*[иiu])?|[уyu][\W_]*ю|[оo0][\W_]*[мm][\W_]*[уyu])))',

    # *хуй*
    '(?:[нhn][\W_]*[иеeiu][\W_]*|[пnp][\W_]*[оo0][\W_]*|[нhn][\W_]*[аa][\W_]*|[оаoa0][\W_]*(?:[тt][\W_]*)?|[дd][\W_]*[аоoa0][\W_]*|[з3z][\W_]*[аa][\W_]*)?(?:(?:[хxh][\W_]*(?:[еиeiu][\W_]*(?:[йj][\W_]*)?[рpr]|[уyu](?:[\W_]*[йj])?))(?:[\W_]*[еоёeo0][\W_]*[вbv](?:[\W_]*[аa][\W_]*ю[\W_]*щ|[\W_]*ш)?)?(?:[\W_]*[аиеeiau][\W_]*[лнlhn])?(?:[нhn])?(?:[\W_]*(?:[иаоёяыеeioau0][юяиевмйbeijmvu]|я[\W_]*(?:[мm](?:[\W_]*[иiu])?|[рpr][\W_]*(?:ю|[иiu][\W_]*(?:[тt](?:[\W_]*[ьеeb][\W_]*[сsc][\W_]*[яьb])?|[лl](?:[\W_]*[иоаioau0])?))|[чc][\W_]*(?:[аиiau][\W_]*[тt](?:[\W_]*[сsc][\W_]*я)|[иiu][\W_]*[лl](?:[\W_]*[иоаioau0])?)|[чc](?:[\W_]*[ьb])?)|[еe][\W_]*(?:[тt][\W_]*(?:[оo0][\W_]*[йj]|[аьуybau])|[еe][\W_]*(?:[тt][\W_]*[еe]|ш[\W_]*[ьb]))|[аыоуяюйиijoyau0]|[лl][\W_]*[иоiou0]|[чc][\W_]*[уyu])))',

    # хуй
    '(?:[хxh][\W_]*(?:[еиeiu][\W_]*(?:[йj][\W_]*)?[рpr]|[уyu][\W_]*[йj]))',

    # хуеc*
    '[хxh][\W_]*[уyu][\W_]*(?:[еёиeiu][\W_]*(?:[сsc][\W_]*[оo0][\W_]*[сsc]|[пnp][\W_]*[лl][\W_]*[еe][\W_]*[тt]|[нhn][\W_]*[ыi][\W_]*ш)(?:[\W_]*[аыуyiau]|[\W_]*[оаoa0][\W_]*[мm](?:[\W_]*[иiu])?|[нhn][\W_]*(?:[ыиiu][\W_]*[йj]|[аa][\W_]*я|[оo0][\W_]*[йеej]|[ыi][\W_]*[хxh]|[ыi][\W_]*[еe]|[ыi][\W_]*[мm](?:[\W_]*[иiu])?|[уyu][\W_]*ю|[оo0][\W_]*[мm][\W_]*[уyu]))?|[дd][\W_]*[оo0][\W_]*ё[\W_]*[бb6][\W_]*[иiu][\W_]*[нhn][\W_]*(?:[оo0][\W_]*[йj]|[аеыуeyiau]))',

    # бляд*
    '(\w*[бb6][\W_]*[лl][\W_]*(я|[еe][аa])(?:[\W_]*[дтdt][ьъ]?[\W_]*(?:[ьb]|[иiu]|[кk][\W_]*[иiu]|[сsc][\W_]*[тt][\W_]*[вbv][\W_]*[оo0]|[сsc][\W_]*[кk][\W_]*(?:[оo0][\W_]*[ейej]|[иiu][\W_]*[еe]|[аa][\W_]*я|[иiu][\W_]*[йj]|[оo0][\W_]*[гrg][\W_]*[оo0])))?)',

    # выбляд*
    '[вbv][\W_]*[ыi][\W_]*[бb6][\W_]*[лl][\W_]*я[\W_]*[дd][\W_]*(?:[оo0][\W_]*[кk]|[кk][\W_]*(?:[иуаеeiyau]|[аa][\W_]*[мm](?:[\W_]*[иiu])?))',

    # западл*
    '(?:[з3z][\W_]*[аоoa0][\W_]*)(?:[пnp][\W_]*[аоoa0][\W_]*[дd][\W_]*[лl][\W_]*[оыаoia0]|[лl][\W_]*[уyu][\W_]*[пnp][\W_]*(?:[оo0][\W_]*[йj]|[аеыуeyiau]))',

    # шлюх*
    'ш[\W_]*[лl][\W_]*ю[\W_]*[хxh][\W_]*(?:[ауеиeiyau]|[оo0][\W_]*[йj])',

    # анус*
    '[аa][\W_]*[нhn][\W_]*[уyu][сsc](?:[\W_]*[еаыуeyiau]|[\W_]*[оo0][\W_]*[мm])?',
)

explicit_list = (
    "нехуй", "мудило",
    "6ля", "6лядь", "6лять", "b3ъeб", "cock", "cunt", "e6aль", "ebal", "eblan", "eбaл", "eбaть", "eбyч", "eбать",
    "eбёт", "eблантий", "fuck", "fucker", "fucking", "xyёв", "xyй", "xyя", "xуе", "xуй", "xую", "zaeb", "zaebal",
    "zaebali", "zaebat", "архипиздрит", "ахуел", "ахуеть", "бздение", "бздеть", "бздех", "бздецы", "бздит",
    "бздицы",
    "бздло", "бзднуть", "бздун", "бздунья", "бздюха", "бздюшка", "бздюшко", r"бля", "блябу", "блябуду", "бляд",
    "бляди",
    "блядина", "блядище", "блядки", "блядовать", "блядство", "блядун", "блядуны", "блядунья", "блядь", "блядюга",
    "блять", "вафел", "вафлёр", "взъебка", "взьебка", "взьебывать", "въеб", "въебался", "въебенн", "въебусь",
    "въебывать", "выблядок", "выблядыш", "выеб", "выебать", "выебен", "выебнулся", "выебон", "выебываться",
    "выпердеть",
    "высраться", "выссаться", "вьебен", "гавно", "гавнюк", "гавнючка", "гамно", "гандон", "гнид", "гнида", "гниды",
    "говенка", "говенный", "говешка", "говназия", "говнецо", "говнище", "говно", "говноед", "говнолинк",
    "говночист",
    "говнюк", "говнюха", "говнядина", "говняк", "говняный", "говнять", "гондон", "доебываться", "долбоеб",
    "долбоёб",
    "долбоящер", "дрисня", "дрист", "дристануть", "дристать", "дристун", "дристуха", "дрочелло", "дрочена",
    "дрочила",
    "дрочилка", "дрочистый", "дрочить", "дрочка", "дрочун", "е6ал", "е6ут", "еб твою мать", "ёб твою мать", "ёбaн",
    "ебaть", "ебyч", "ебал", "ебало", "ебальник", "ебан", "ебанамать", "ебанат", "ебаная", "ёбаная", "ебанический",
    "ебанный", "ебанныйврот", "ебаное", "ебануть", "ебануться", "ёбаную", "ебаный", "ебанько", "ебарь", "ебат",
    "ёбат",
    "ебатория", "ебать", "ебать-копать", "ебаться", "ебашить", "ебёна", "ебет", "ебёт", "ебец", "ебик", "ебин",
    "ебись",
    "ебическая", "ебки", "ебла", "еблан", "ебливый", "еблище", "ебло", "еблыст", "ебля", "ёбн", "ебнуть",
    "ебнуться",
    "ебня", "ебошить", "ебская", "ебский", "ебтвоюмать", "ебун", "ебут", "ебуч", "ебуче", "ебучее", "ебучий",
    "ебучим",
    "ебущ", "ебырь", "елда", "елдак", "елдачить", "жопа", "жопу", "заговнять", "задрачивать", "задристать",
    "задрота",
    "зае6", "заё6", "заеб", "заёб", "заеба", "заебал", "заебанец", "заебастая", "заебастый", "заебать", "заебаться",
    "заебашить", "заебистое", "заёбистое", "заебистые", "заёбистые", "заебистый", "заёбистый", "заебись",
    "заебошить",
    "заебываться", "залуп", "залупа", "залупаться", "залупить", "залупиться", "замудохаться", "запиздячить",
    "засерать",
    "засерун", "засеря", "засирать", "засрун", "захуячить", "заябестая", "злоеб", "злоебучая", "злоебучее",
    "злоебучий",
    "ибанамат", "ибонех", "изговнять", "изговняться", "изъебнуться", "ипать", "ипаться", "ипаццо",
    "Какдвапальцаобоссать", "конча", "курва", "курвятник", "лох", "лошарa", "лошара", "лошары", "лошок", "лярва",
    "малафья", "манда", "мандавошек", "мандавошка", "мандавошки", "мандей", "мандень", "мандеть", "мандища",
    "мандой",
    "манду", "мандюк", "минет", "минетчик", "минетчица", "млять", "мокрощелка", "мокрощёлка", "мразь", "мудak",
    "мудaк",
    "мудаг", "мудак", "муде", "мудель", "мудеть", "муди", "мудил", "мудила", "мудистый", "мудня", "мудоеб",
    "мудозвон",
    "мудоклюй", "на хер", "на хуй", "набздел", "набздеть", "наговнять", "надристать", "надрочить", "наебать",
    "наебет",
    "наебнуть", "наебнуться", "наебывать", "напиздел", "напиздели", "напиздело", "напиздили", "насрать",
    "настопиздить",
    "нахер", "нахрен", "нахуй", "нахуйник", "не ебет", "не ебёт", "невротебучий", "невъебенно", "нехира", "нехрен",
    "Нехуй", "нехуйственно", "ниибацо", "ниипацца", "ниипаццо", "ниипет", "никуя", "нихера", "нихуя",
    "обдристаться",
    "обосранец", "обосрать", "обосцать", "обосцаться", "обсирать", "объебос", "обьебать", "обьебос", "однохуйственно",
    "опездал", "опизде", "опизденивающе", "остоебенить", "остопиздеть", "отмудохать", "отпиздить", "отпиздячить",
    "отпороть", "отъебись", "охуевательский", "охуевать", "охуевающий", "охуел", "охуенно", "охуеньчик", "охуеть",
    "охуительно", "охуительный", "охуяньчик", "охуячивать", "охуячить", "очкун", "падла", "падонки", "падонок",
    "паскуда", "педерас", "педик", "педрик", "педрила", "педрилло", "педрило", "педрилы", "пездень", "пездит",
    "пездишь", "пездо", "пездят", "пердануть", "пердеж", "пердение", "пердеть", "пердильник", "перднуть",
    "пёрднуть",
    "пердун", "пердунец", "пердунина", "пердунья", "пердуха", "пердь", "переёбок", "пернуть", "пёрнуть", "пи3д",
    "пи3де", "пи3ду", "пиzдец", "пидар", "пидарaс", "пидарас", "пидарасы", "пидары", "пидор", "пидорасы", "пидорка",
    "пидорок", "пидоры", "пидрас", "пизда", "пиздануть", "пиздануться", "пиздарваньчик", "пиздато", "пиздатое",
    "пиздатый", "пизденка", "пизденыш", "пиздёныш", "пиздеть", "пиздец", "пиздит", "пиздить", "пиздиться",
    "пиздишь", "пидр",
    "пиздища", "пиздище", "пиздобол", "пиздоболы", "пиздобратия", "пиздоватая", "пиздоватый", "пиздолиз",
    "пиздонутые",
    "пиздорванец", "пиздорванка", "пиздострадатель", "пизду", "пиздуй", "пиздун", "пиздунья", "пизды", "пиздюга",
    "пиздюк", "пиздюлина", "пиздюля", "пиздят", "пиздячить", "писбшки", "писька", "писькострадатель", "писюн",
    "писюшка", "по хуй", "по хую", "подговнять", "подонки", "подонок", "подъебнуть", "подъебнуться", "поебать",
    "поебень", "поёбываает", "поскуда", "посрать", "потаскуха", "потаскушка", "похер", "похерил", "похерила",
    "похерили", "похеру", "похрен", "похрену", "похуй", "похуист", "похуистка", "похую", "придурок", "приебаться",
    "припиздень", "припизднутый", "припиздюлина", "пробзделся", "проблядь", "проеб", "проебанка", "проебать",
    "промандеть", "промудеть", "пропизделся", "пропиздеть", "пропиздячить", "раздолбай", "разхуячить", "разъеб",
    "разъеба", "разъебай", "разъебать", "распиздай", "распиздеться", "распиздяй", "распиздяйство", "распроеть",
    "сволота", "сволочь", "сговнять", "секель", "серун", "серька", "сестроеб", "сикель", "сила", "сирать",
    "сирывать",
    "соси", "спиздел", "спиздеть", "спиздил", "спиздила", "спиздили", "спиздит", "спиздить", "срака", "сраку",
    "сраный",
    "сранье", "срать", "срун", "ссака", "ссышь", "стерва", "страхопиздище", "сука", "суки", "суходрочка", "сучара",
    "сучий", "сучка", "сучко", "сучонок", "сучье", "сцание", "сцать", "сцука", "сцуки", "сцуконах", "сцуль",
    "сцыха",
    "сцышь", "съебаться", "сыкун", "трахае6", "трахаеб", "трахаёб", "трахатель", "ублюдок", "уебать", "уёбища",
    "уебище", "уёбище", "уебищное", "уёбищное", "уебк", "уебки", "уёбки", "уебок", "уёбок", "урюк", "усраться",
    "ушлепок", "х_у_я_р_а", "хyё", "хyй", "хyйня", "хамло", "хер", "херня", "херовато", "херовина", "херовый",
    "хитровыебанный", "хитрожопый", "хуeм", "хуе", "хуё", "хуевато", "хуёвенький", "хуевина", "хуево", "хуевый",
    "хуёвый", "хуек", "хуёк", "хуел", "хуем", "хуенч", "хуеныш", "хуенький", "хуеплет", "хуеплёт",
    "хуепромышленник",
    "хуерик", "хуерыло", "хуесос", "хуесоска", "хуета", "хуетень", "хуею", "хуи", "хуй", "хуйком", "хуйло", "хуйня",
    "хуйрик", "хуище", "хуля", "хую", "хуюл", "хуя", "хуяк", "хуякать", "хуякнуть", "хуяра", "хуясе", "хуячить",
    "целка", "чмо", "чмошник", "чмырь", "шалава", "шалавой", "шараёбиться", "шлюха", "шлюхой", "шлюшка", "ябывает",
    'пiзда',
)

exclude_list = (
    'сабля', 'употреблять', 'рубля', 'злоупотреблять'
)


async def find_explicit(text: str):
    patterns = my_patterns + external_patterns

    for pattern in patterns:
        to_find = re.compile(pattern, flags=re.IGNORECASE)
        result = re.search(to_find, text)

        if result:
            word = result.group()

            if word in exclude_list:
                continue

            logger.info(f'{word} - {pattern}')
            return True

    return False
