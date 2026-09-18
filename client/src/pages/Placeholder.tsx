

export const Placeholder = ({ title }: { title: string }) => {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center">
      <h2 className="text-3xl font-bold text-slate-100 mb-4">{title}</h2>
      <p className="text-zinc-400 max-w-md">
        This feature is currently in development. The underlying machine learning models are being evaluated and will be deployed soon.
      </p>
      <div className="mt-8 p-6 bg-zinc-900/50 rounded-xl border border-zinc-800 max-w-lg w-full">
        <div className="animate-pulse flex space-x-4">
          <div className="flex-1 space-y-4 py-1">
            <div className="h-4 bg-zinc-800 rounded w-3/4"></div>
            <div className="space-y-2">
              <div className="h-4 bg-zinc-800 rounded"></div>
              <div className="h-4 bg-zinc-800 rounded w-5/6"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
