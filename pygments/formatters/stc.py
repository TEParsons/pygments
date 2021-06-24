from pygments.formatter import Formatter
import pygments.token
import pygments.style
import re


class StcFormatter(Formatter):
    """
    Applies a pygments style to a `wx.stc.StyledTextCtrl` object. Unlike other formatters, does not output anything - instead applies style to the object given to the `format` function

    .. versionadded:: 2.9.0
    """

    supported_lexers = [
        2,  # Python
        3,  # C++
        4,  # HTML
        48,  # YAML
        86,  # R
        120,  # JSON
    ]

    def format(self, target):
        """
        Format ``target``, a `wx.stc.StyledTextCtrl` object.
        """
        try:
            import wx.stc
        except ImportError:
            raise ImportError("Creating an stc formatter requires wx to be installed")

        assert isinstance(self.style, pygments.style.Style), f"Style object must be a pygments.style.Style"
        assert isinstance(target, wx.stc.StyledTextCtrl), f"Target object must be a wx.stc.StyledTextCtrl"
        assert target.GetLexer() in self.supported_lexers, f"Language '{target.GetLexerLanguage()}' not currently supported"

        target.SetBackgroundColour(self.style.background_color)
        # Set selection colour
        target.SetSelBackground(self.style.highlight_color)
        # Set margin
        target.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER, self.style.line_number_color)
        target.SetFoldMarginColour(True, self.style.line_number_background_color)
        target.SetFoldMarginHiColour(True, self.style.line_number_special_background_color)

        # Map pygments tokens to stc tokens
        token_map = {
            pygments.token.Text: [getattr(wx.stc, key) for key in dir(wx.stc) if "_DEFAULT" in key] + [wx.stc.STC_YAML_TEXT],
            pygments.token.Text.Whitespace: [wx.stc.STC_STYLE_INDENTGUIDE],
            pygments.token.Escape: [],
            pygments.token.Keyword: [wx.stc.STC_P_WORD, wx.stc.STC_C_WORD, wx.stc.STC_YAML_KEYWORD, wx.stc.STC_R_KWORD,wx.stc.STC_R_BASEKWORD, wx.stc.STC_JSON_KEYWORD],
            pygments.token.Keyword.Constant: [],
            pygments.token.Keyword.Declaration: [wx.stc.STC_P_DEFNAME],
            pygments.token.Keyword.Namespace: [],
            pygments.token.Keyword.Pseudo: [],
            pygments.token.Keyword.Reserved: [wx.stc.STC_P_WORD2, wx.stc.STC_C_WORD2, wx.stc.STC_R_OTHERKWORD],
            pygments.token.Keyword.Type: [],
            pygments.token.Name: [],
            pygments.token.Name.Attribute: [],
            pygments.token.Name.Builtin: [],
            pygments.token.Name.Builtin.Pseudo: [],
            pygments.token.Name.Class: [wx.stc.STC_P_CLASSNAME],
            pygments.token.Name.Constant: [],
            pygments.token.Name.Decorator: [wx.stc.STC_P_DECORATOR],
            pygments.token.Name.Entity: [],
            pygments.token.Name.Exception: [],
            pygments.token.Name.Function: [],
            pygments.token.Name.Function.Magic: [],
            pygments.token.Name.Property: [wx.stc.STC_JSON_PROPERTYNAME],
            pygments.token.Name.Label: [],
            pygments.token.Name.Namespace: [],
            pygments.token.Name.Other: [],
            pygments.token.Name.Tag: [wx.stc.STC_T3_HTML_TAG],
            pygments.token.Name.Variable: [wx.stc.STC_P_IDENTIFIER, wx.stc.STC_C_IDENTIFIER, wx.stc.STC_YAML_IDENTIFIER, wx.stc.STC_R_IDENTIFIER],
            pygments.token.Name.Variable.Class: [wx.stc.STC_C_GLOBALCLASS],
            pygments.token.Name.Variable.Global: [],
            pygments.token.Name.Variable.Instance: [],
            pygments.token.Name.Variable.Magic: [],
            pygments.token.Literal: [wx.stc.STC_C_USERLITERAL],
            pygments.token.Literal.Date: [],
            pygments.token.Literal.String: [wx.stc.STC_P_STRING, wx.stc.STC_C_STRING, wx.stc.STC_T3_HTML_STRING, wx.stc.STC_JSON_STRING, wx.stc.STC_R_STRING],
            pygments.token.Literal.String.Affix: [],
            pygments.token.Literal.String.Backtick: [],
            pygments.token.Literal.String.Char: [wx.stc.STC_P_CHARACTER, wx.stc.STC_C_CHARACTER],
            pygments.token.Literal.String.Delimiter: [],
            pygments.token.Literal.String.Doc: [wx.stc.STC_P_TRIPLE, wx.stc.STC_P_TRIPLEDOUBLE, wx.stc.STC_C_COMMENTDOC, wx.stc.STC_YAML_DOCUMENT],
            pygments.token.Literal.String.Double: [wx.stc.STC_R_STRING2],
            pygments.token.Literal.String.Escape: [wx.stc.STC_C_ESCAPESEQUENCE],
            pygments.token.Literal.String.Heredoc: [],
            pygments.token.Literal.String.Interpol: [],
            pygments.token.Literal.String.Other: [],
            pygments.token.Literal.String.Regex: [wx.stc.STC_C_REGEX],
            pygments.token.Literal.String.Single: [],
            pygments.token.Literal.String.Symbol: [],
            pygments.token.Literal.Number: [wx.stc.STC_P_NUMBER, wx.stc.STC_C_NUMBER, wx.stc.STC_YAML_NUMBER, wx.stc.STC_R_NUMBER, wx.stc.STC_JSON_NUMBER],
            pygments.token.Literal.Number.Bin: [],
            pygments.token.Literal.Number.Float: [],
            pygments.token.Literal.Number.Hex: [],
            pygments.token.Literal.Number.Integer: [],
            pygments.token.Literal.Number.Integer.Long: [],
            pygments.token.Literal.Number.Oct: [],
            pygments.token.Operator: [wx.stc.STC_P_OPERATOR, wx.stc.STC_C_OPERATOR, wx.stc.STC_YAML_OPERATOR, wx.stc.STC_R_OPERATOR, wx.stc.STC_JSON_OPERATOR],
            pygments.token.Operator.Word: [],
            pygments.token.Punctuation: [],
            pygments.token.Comment: [wx.stc.STC_C_COMMENT, wx.stc.STC_YAML_COMMENT, wx.stc.STC_R_COMMENT],
            pygments.token.Comment.Hashbang: [wx.stc.STC_C_HASHQUOTEDSTRING],
            pygments.token.Comment.Multiline: [wx.stc.STC_P_COMMENTBLOCK, wx.stc.STC_JSON_BLOCKCOMMENT],
            pygments.token.Comment.Preproc: [wx.stc.STC_C_PREPROCESSORCOMMENT],
            pygments.token.Comment.PreprocFile: [wx.stc.STC_C_PREPROCESSORCOMMENTDOC],
            pygments.token.Comment.Single: [wx.stc.STC_P_COMMENTLINE, wx.stc.STC_C_COMMENTLINE],
            pygments.token.Comment.Special: [],
            pygments.token.Generic: [],
            pygments.token.Generic.Deleted: [],
            pygments.token.Generic.Emph: [],
            pygments.token.Generic.Error: [wx.stc.STC_STYLE_BRACEBAD, wx.stc.STC_JSON_ERROR, wx.stc.STC_YAML_ERROR],
            pygments.token.Generic.Heading: [],
            pygments.token.Generic.Inserted: [],
            pygments.token.Generic.Output: [],
            pygments.token.Generic.Prompt: [],
            pygments.token.Generic.Strong: [],
            pygments.token.Generic.Subheading: [],
            pygments.token.Generic.Traceback: [],
            pygments.token.Other: [
                # Uncaught
                wx.stc.STC_P_STRINGEOL,
                wx.stc.STC_C_COMMENTDOCKEYWORD,
                wx.stc.STC_C_COMMENTDOCKEYWORDERROR,
                wx.stc.STC_C_COMMENTLINEDOC,
                wx.stc.STC_C_PREPROCESSOR,
                wx.stc.STC_C_STRINGEOL,
                wx.stc.STC_C_STRINGRAW,
                wx.stc.STC_C_TASKMARKER,
                wx.stc.STC_C_TRIPLEVERBATIM,
                wx.stc.STC_C_UUID,
                wx.stc.STC_C_VERBATIM,
                wx.stc.STC_YAML_REFERENCE,
                wx.stc.STC_R_INFIX,
                wx.stc.STC_R_INFIXEOL,
                wx.stc.STC_JSON_COMPACTIRI,
                wx.stc.STC_JSON_ESCAPESEQUENCE,
                wx.stc.STC_JSON_LDKEYWORD,
                wx.stc.STC_JSON_LINECOMMENT,
                wx.stc.STC_JSON_STRINGEOL,
                wx.stc.STC_JSON_URI,
                wx.stc.STC_STYLE_BRACELIGHT,
                wx.stc.STC_STYLE_CALLTIP,
                wx.stc.STC_STYLE_CONTROLCHAR,
                wx.stc.STC_STYLE_FOLDDISPLAYTEXT,
                wx.stc.STC_STYLE_LASTPREDEFINED,
                wx.stc.STC_STYLE_MAX,
            ],
        }
        # Iterate through style and apply based on token map
        for key, value in self.style.styles.items():
            # Skip if key isn't mapped
            if key not in token_map:
                continue
            # Apply style for each alias
            for alias in token_map[key]:
                target.StyleSetSpec(alias, self.pygments2stc(value))

    @staticmethod
    def pygments2stc(spec):
        """
        Convert a pygments-style spec string to a wx.stc-style spec string
        """

        # Extract attributes from pygments spec
        bold = re.match(r"bold", spec)
        nobold = re.match(r"nobold", spec)
        italic = re.match(r"italic", spec)
        noitalic = re.match(r"noitalic", spec)
        underline = re.match(r"underline", spec)
        nounderline = re.match(r"nounderline", spec)
        noinherit = re.match(r"noinherit", spec)
        bg = re.match(r"(?<=bg:) ?[0-9abcdef]{0,3}", spec)
        border = re.match(r"(?<=border:) ?#?[0-9abcdef]{0,6}", spec)
        fg = re.match(r"(?<!:)#[0-9abcdef]{0,6}", spec)
        # Use extracted attributes to build stc spec
        out = []
        if fg:
            out.append("fore:" + fg.string)
        if bg:
            if bg.string:
                out.append("back:" + bg.string)
            else:
                out.append("back:None")
        if bold and not nobold:
            out.append("bold")
        if italic and not noitalic:
            out.append("italic")

        return " ".join(out)
