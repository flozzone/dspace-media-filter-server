from preview_generator.manager import PreviewManager

from dspace_media_filter.filter import MediaFilter, MediaFilterResponse, MediaFilterRequest


class ThumbnailFilter(MediaFilter):

    def __init__(self, cache_dir=None):
        super().__init__(cache_dir=cache_dir)
        self.manager = PreviewManager(cache_folder_path=self.cache_dir, create_folder=True)

    def filter(self, req: MediaFilterRequest) -> MediaFilterResponse:
        return MediaFilterResponse(result_file_path=self.manager.get_jpeg_preview(req.abs_file))
