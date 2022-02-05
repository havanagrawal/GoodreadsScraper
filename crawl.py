import click
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


@click.group()
@click.option("--log_file",
              help="Log file for scrapy logs",
              type=str,
              default="scrapy.log",
              show_default=True)
@click.pass_context
def crawl(ctx, log_file="scrapy.log"):
    ctx.ensure_object(dict)
    ctx.obj['LOG_FILE'] = log_file


@crawl.command()
@click.option(
    "--list_name",
    required=True,
    help=
    "Goodreads Listopia list name. It can be determined from the URL of the list. For e.g. the name of the list https://www.goodreads.com/list/show/1.Best_Books_Ever is '1.Best_Books_Ever'",
    type=str)
@click.option("--start_page",
              help="Start page number",
              default=1,
              type=int,
              show_default=True)
@click.option("--end_page", required=True, help="End page number", type=int)
@click.option("--output_file_suffix",
              help="The suffix for the output file. Defaults to the list name",
              type=str)
@click.pass_context
def list(ctx, list_name: str, start_page: int, end_page: int,
         output_file_suffix):
    """Crawl a Goodreads Listopia List.

    Crawl all pages between start_page and end_page (inclusive) of a Goodreads Listopia List.

    \b
    By default, two files will be created:
      1.   book_{output_file_suffix}.jl, for books from the given list
      2.   author_{output_file_suffix}.jl, for authors of the above books from the given list
    """
    if not output_file_suffix:
        output_file_suffix = list_name
    click.echo(
        f"Crawling Goodreads list {list_name} for pages [{start_page}, {end_page}]"
    )

    _crawl('list',
           ctx.obj["LOG_FILE"],
           output_file_suffix,
           list_name=list_name,
           start_page_no=start_page,
           end_page_no=end_page)


@crawl.command()
@click.option("--output_file_suffix",
              help="The suffix for the output file. Defaults to 'all'",
              type=str)
@click.pass_context
def author(ctx, output_file_suffix='all'):
    """Crawl all authors on Goodreads.

    [IMPORTANT]: This command will only complete after it has crawled
    ALL the authors on Goodreads, which may be a long time.
    For all intents and purposes, treat this command as a never-terminating one
    that will block the command-line forever.

    It is STRONGLY RECOMMENDED that you either terminate it manually (with an interrupt) or
    run it in the background.
    """
    click.echo("Crawling Goodreads for all authors")
    click.echo(
        click.style(
            "[WARNING] This command will block the CLI, and never complete (unless interrupted)",
            fg='red'))

    _crawl('author',
           ctx.obj["LOG_FILE"],
           output_file_suffix,
           author_crawl=True)


def _crawl(spider_name, log_file, output_file_suffix, **crawl_kwargs):
    settings = get_project_settings()

    # used by the JsonLineItem pipeline
    settings.set("OUTPUT_FILE_SUFFIX", output_file_suffix)

    # Emit all scrapy logs to log_file instead of stderr
    settings.set("LOG_FILE", log_file)

    process = CrawlerProcess(settings)

    process.crawl(spider_name, **crawl_kwargs)

    # CLI will block until this call completes
    process.start()


if __name__ == "__main__":
    crawl()
