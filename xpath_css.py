from scrapy import Selector

# made a little change in html code.
html = """
<html>
  <body>
    <div class='hello_world'>
      <p>Hello World!</p>
      <div id='choose_me'>
        <p>Choose me!</p>
      </div>
    </div>
    <div>
      <p>Why are you not looking at me?</p>
    </div>
    <div>
      This is a sentence.
      <a href='www.google.com'>click here</a> it will take you to the another website.
    </div>
  </body>
</html>
"""

sel = Selector(text=html)

#----------------------------------------------------------------------------------------------------------------
# Selecting class
# ---------------------------------------------------------------------------------------------------------------
xpath = '//div[@class="hello_world"]/p' # here we are selecting all the divs which has a class named "hello_world"
print(sel.xpath(xpath).xpath('./text()').extract())

css = 'div.hello_world > p' # same for css but this time we don't have to use square brackets or @
                            # just we have to use '.' before class name. If you are familiar with writing css
                            # this part will be easier for you to understand.

print(sel.css(css).css('::text').extract())

# both prints "Hello World!", as there is only one div tag where the class name is "hello_world"

# ----------------------------------------------------------------------------------------------------------------
# Selecting id
# ----------------------------------------------------------------------------------------------------------------

xpath = '//div[@id="choose_me"]/p' # selecting all div tags where id name is "choose_me"
print(sel.xpath(xpath).xpath('./text()').extract())

css = 'div#choose_me > p' # here we have to give a '#' sign before the id name.
print(sel.css(css).css('::text').extract())

# both prints "Choose me!" as there is only one div tag where id name is "choose_me"
