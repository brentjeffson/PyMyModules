from bs4 import BeautifulSoup
import os

API_KEY = os.environ.get('YTAPI')

class Youtube:

    @staticmethod
    def search(keyword):
        

    @staticmethod
    def get_sources(html, parser='html.parser'):
        '''Parses Youtube html to get available video sources
        Args:
            html (str): Youtube html to be parsed
            parser (:obj:`str`, optional): Parser to be used by BeautifulSoup to parse the html. Defaults to `html.parser`

        Returns:
            video_info (list[dict]): List of video sources with meta
        ''' 
        # parses html to a BeautifulSoup object
        soup = BeautifulSoup(html, parser)

        # find script containing video informations
        player_script_tag = soup.select("div#player script:nth-of-type(2)")
        
        # find the sources using regex
        pattern = r'formats\\":(.+)(}]|}]}),\\"(playerAds|dashManifestUrl)'
        searched = re.search(pattern, player_script_tag[0].text)

        # do some cleaning
        src = searched.groups()[0]
        clean_src = src.replace("\\u0026", "&").replace('\\', '')#.replace('[{', '').replace('}}]', '')

        # split cleaned src
        url_info = []
        for index, p in enumerate(re.split("},{", clean_src)):   
            
            # remove excess closing tags
            if index == 0: 
                p = p.replace("[{", "")
            elif index == len(re.split("},{", clean_src))-1:
                p = p.replace("}]}", "")
        
            codecs_value = re.search(r"codecs=\"([\w,\s.\-?_]+)\"", p).groups()[0]
            new_str = re.sub(r'codecs=".+"",', f"codecs={codecs_value}\",", p)
            
            # convert to dictionary, add to list           
            url_info.append(json.loads("{" + new_str + "}"))
        return url_info




