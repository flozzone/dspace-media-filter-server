from preview_generator.manager import PreviewManager

from dspace_media_filter.filter import MediaFilter, MediaFilterResponse, MediaFilterRequest

cache_path = '/tmp/preview_cache'


class ThumbnailFilter(MediaFilter):
    manager = PreviewManager(cache_path, create_folder=True)

    def filter(self, req: MediaFilterRequest) -> MediaFilterResponse:
        return MediaFilterResponse(result_file_path=self.manager.get_jpeg_preview(req.abs_file))
